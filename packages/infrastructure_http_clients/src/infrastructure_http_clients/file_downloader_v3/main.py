import os
from typing import Callable
import aiohttp, asyncio
from pathlib import Path
from aiohttp import ClientTimeout

from infrastructure_http_clients.file_downloader_v3.downloader import download_file
from infrastructure_http_clients.file_downloader_v3.exceptions import DownloadErr
from infrastructure_http_clients.file_downloader_v3.shemas import DownloadTask
from infrastructure_http_clients.file_downloader_v3.funcs import check_zip_integrity, check_tar_gz_integrity


async def downolad_many_files(
        root_dir: Path, dwn_tasks: list[DownloadTask], event: asyncio.Event, feedback_dict: dict,
        limit_tasks: int = 2, retries: int = 4, retries_timeout: float = 3,
        retries_callback: Callable[[str], None] | None = None,
        error_callback: Callable[[str], None] | None = None,
) -> None:
    """
    :param root_dir:  корневая директория проекта
    :param dwn_tasks: задача на загрузку
    :param event: событие выхода (срочная остановка загрузок)
    :param feedback_dict: обратная связь, хранит в себе прогресс загружаемых файлоы
    :param limit_tasks: максимум загрузок за 1 заход
    :param retries: количество попыток переподключения (если соединение разорвано или ошибки сети -> работает только для тех ситуаций когда размер файла получен от сервера, например через заголовок)
    :param retries_timeout: временной интервал между попытками переподключения (сек)
    :param retries_callback: в случае новой попытки подключения и загрузки отработает эта функция, в арумент прочитается сообщение msg
    :param error_callback: если при загрузке возникла какая либо ошибка, то отработает этот коллбэк передав в него текст ошибки
    """
    # ограниченная по скорости закачка, так как много закачек сразу блокируют каналы
    semaphore = asyncio.Semaphore(limit_tasks)

    async def download_with_limit(dwn, session_in):
        async with semaphore:
            return await download_file(
                event=event,
                session=session_in,
                feedback_dict=feedback_dict,
                **dwn.get_downloader(root_dir=root_dir)
            )

    timeout = ClientTimeout(
        total=None,  # самое важное, иначе aiohttp рвет соединение-сессию через 5 минут (критично для больших файлов)
        connect=30,
        sock_read=30,  # защита от зависания когда чанк не приходит
        sock_connect=30,
    )

    async with aiohttp.ClientSession(timeout=timeout) as session:
        r = 0
        while dwn_tasks:
            results = await asyncio.gather(
                *[download_with_limit(dwn, session_in=session) for dwn in dwn_tasks], return_exceptions=True
            )

            if event.is_set() or r >= retries:
                event.set()  # на всякий случай, если выход был через retries
                break

            error_task = False
            text_err = ''
            remaining_tasks = []  # новый список для тех, кто не докачался

            for i, (task, result) in enumerate(zip(dwn_tasks, results)):
                if isinstance(result, DownloadErr.Break):
                    text_err = f'✔ {task.label} отменено'
                elif isinstance(result, DownloadErr.TimeoutError):
                    error_task = True
                    text_err = f'❌ {task.label}: истёк таймаут загрузки'
                elif isinstance(result, DownloadErr.StatusError):
                    error_task = True
                    text_err = f'❌ {task.label}: ошибка сервера'
                elif isinstance(result, Exception):
                    error_task = True
                    text_err = f'❌ {task.label}: {result}'

                if error_task:
                    if error_callback is not None:
                        error_callback(text_err)  # пробросить сообщение об ошибке наверх (для логирования например)
                    remaining_tasks.append(task)  # Если при загрузке какая либо ошибка оставить на следующий круг
                    continue

                # проверка целостности файлов (пока только zip, tar.gz)
                file_path = root_dir / task.relative_path_file
                corrupted = False
                if file_path.suffix == '.zip':
                    try:
                        # проверить целостность zip
                        check_zip_integrity(path_archive=file_path)
                    except Exception as err:  # noqa
                        # архив битый удалить его (это временная мера, но для битых архивов git пока это палочка выручалочка)
                        corrupted = True
                if file_path.name.endswith('.tar.gz'):
                    try:
                        # проверить целостность zip
                        check_tar_gz_integrity(path_archive=file_path)
                    except Exception as err:  # noqa
                        # архив битый удалить его (это временная мера, но для битых архивов git пока это палочка выручалочка)
                        corrupted = True

                if corrupted:
                    if error_callback is not None:
                        error_callback(f'Архив {task.label}, битый, качаю заново.')
                    if file_path.exists():
                        os.remove(file_path)
                    feedback_dict[task.label]['progress'] = 0
                    feedback_dict[task.label]['downolad'] = 0
                    remaining_tasks.append(task)
                    continue

                # проверка что файл докачан (для тех кто не проходит проверку на целостность)
                if feedback_dict[task.label]['total'] != 0:
                    if feedback_dict[task.label]['progress'] == 100:
                        pass
                    else:
                        remaining_tasks.append(task)  # не докачано, оставить на 2 круг
                else:
                    pass  # размер неизвестен, считать скачанным

            dwn_tasks = remaining_tasks  # заменить список на новый
            # задержка перед уходом на 2 круг
            await asyncio.sleep(retries_timeout)
            r += 1

            if dwn_tasks and retries_callback is not None:
                msg = f'Новый круг {r}/{retries} загрузки, догрузка элементов:{[d.label for d in dwn_tasks]}'
                retries_callback(msg)  # новая попытка подключения

        # если осталась хоть одна не решенная задача
        if dwn_tasks:
            raise RuntimeError(f'Не всё удалось загрузить в заданные retries')


async def main():
    from infrastructure_http_clients.file_downloader_v3.utils import observer

    # список заданий на загрузку
    dwn_tasks: list[DownloadTask] = [
        DownloadTask(
            url="https://huggingface.co/Systran/faster-whisper-tiny/resolve/main/model.bin",
            relative_path_file="resources/models/tiny/model.bin",
            label="tiny/model.bin",
        ),
        DownloadTask(
            url="https://huggingface.co/lmstudio-community/gemma-3-1b-it-GGUF/resolve/main/gemma-3-1b-it-Q4_K_M.gguf",
            relative_path_file="resources/models/gemma-3-1b-it-Q4_K_M.gguf",
            label="gemma-3-1b-it-Q4_K_M.gguf",
        ),
    ]

    event = asyncio.Event()  # переменная общего управления циклом загрузки, можно разом отменить всё

    feedback_dict = {
        dwn.label: {'progress': 0.0, 'total': 0, 'downolad': 0} for dwn in dwn_tasks
    }  # для наблюдения за прогрессом обязательно передать feedback_dict, который будет показывать прогресс

    download_task = asyncio.create_task(
        downolad_many_files(root_dir=Path.cwd(), dwn_tasks=dwn_tasks, event=event, feedback_dict=feedback_dict)
    )
    observer_task = asyncio.create_task(observer(feedback_dict_in=feedback_dict, event_in=event))
    await asyncio.sleep(4)
    event.set()
    await download_task
    event.set()
    await observer_task


if __name__ == '__main__':
    asyncio.run(main())
