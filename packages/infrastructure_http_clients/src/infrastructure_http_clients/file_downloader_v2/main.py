import aiohttp, asyncio
from pathlib import Path
from aiohttp import ClientTimeout

from infrastructure_http_clients.file_downloader_v2.downloader import download_file
from infrastructure_http_clients.file_downloader_v2.exceptions import DownloadErr
from infrastructure_http_clients.file_downloader_v2.shemas import DownloadTask


async def downolad_many_files(
        dwn_tasks: list[DownloadTask], event: asyncio.Event, feedback_dict: dict[str, float], limit_tasks: int = 2,
):
    # ограниченная по скорости закачка, так как много закачек сразу блокируют каналы
    semaphore = asyncio.Semaphore(limit_tasks)

    async def download_with_limit(dwn, session_in):
        async with semaphore:
            return await download_file(
                event=event,
                session=session_in,
                feedback_dict=feedback_dict,
                **dwn.get_downloader(root_dir=Path.cwd())
            )

    timeout = ClientTimeout(
        total=None,  # самое важное, иначе aiohttp рвет соединение-сессию через 5 минут (критично для больших файлов)
        connect=30,
        sock_read=30,
        sock_connect=30,
    )

    async with aiohttp.ClientSession(timeout=timeout) as session:
        results = await asyncio.gather(
            *[download_with_limit(dwn, session_in=session) for dwn in dwn_tasks], return_exceptions=True
        )
        for task, result in zip(dwn_tasks, results):
            if isinstance(result, DownloadErr.Break):
                print(f'✔ {task.label} отменено')
            elif isinstance(result, DownloadErr.TimeoutError):
                print(f'❌ {task.label}: истёк таймаут загрузки')
            elif isinstance(result, DownloadErr.StatusError):
                print(f'❌ {task.label}: ошибка сервера')
            elif isinstance(result, Exception):
                print(f'❌ {task.label}: {result}')


async def main():
    from infrastructure_http_clients.file_downloader_v2.utils import observer

    # список заданий на загрузку
    dwn_tasks: list[DownloadTask] = [
        DownloadTask(
            url="https://huggingface.co/Systran/faster-whisper-tiny/resolve/main/model.bin",
            relative_path_file="srv_stt/resources/models/tiny/model.bin",
            label="tiny/model.bin",
        ),
        DownloadTask(
            url="https://huggingface.co/lmstudio-community/gemma-3-1b-it-GGUF/resolve/main/gemma-3-1b-it-Q4_K_M.gguf",
            relative_path_file="srv_llm/resources/models/gemma-3-1b-it-Q4_K_M.gguf",
            label="gemma-3-1b-it-Q4_K_M.gguf",
        ),
    ]

    event = asyncio.Event()  # переменная общего управления циклом загрузки, можно разом отменить всё
    feedback_dict = {dwn.label: 0.0 for dwn in dwn_tasks}  # список загрузок, для отображения процесса
    download_task = asyncio.create_task(
        downolad_many_files(dwn_tasks=dwn_tasks, event=event, feedback_dict=feedback_dict)
    )
    observer_task = asyncio.create_task(observer(feedback_dict_in=feedback_dict, event_in=event))
    await asyncio.sleep(4)
    event.set()
    await download_task
    event.set()
    await observer_task


if __name__ == '__main__':
    asyncio.run(main())
