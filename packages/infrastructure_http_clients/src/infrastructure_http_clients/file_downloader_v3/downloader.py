import asyncio, aiohttp
import hashlib
import os
from aiohttp import ClientTimeout
from pathlib import Path
from infrastructure_http_clients.file_downloader_v3.downloader_get_total_size import get_total_size
from infrastructure_http_clients.file_downloader_v3.exceptions import DownloadErr
from infrastructure_http_clients.file_downloader_v3.sha256_checker import Sha256Checker


async def download_file(
        session: aiohttp.ClientSession, url: str, file_path: Path, label: str, event: asyncio.Event,
        feedback_dict: dict, special_dict: dict, sha256: str | None,
        primary_check_sha256: bool = True,
) -> bool:
    """
    Загрузка одного конкретного файла, с несколькими попытками на чанк в случае ошибки
    :param special_dict:
    :param session:
    :param feedback_dict: словарь очередей
    :param label: название загружаемого файла, может не совпадать с file_path это просто шильдик для словаря в queue_feedback
    :param url: ссылка на файл, например: https://huggingface.co/Systran/faster-whisper-tiny/resolve/main/model.bin
    :param file_path: путь к файлу, для url, например (для url из примера выше): target_dir / model.bin
    :param event: событие остановки (event.is_set())
    :param sha256: проверочный хеш.
    :param primary_check_sha256: первичная проверка sha256.
    :return: bool
    """

    lock = asyncio.Lock()
    tolerance = 1024 * 1024  # 1mb
    chunk_timeout = 2  # время на ожидание одного чанка
    chunksize = 16 * 1024  # 16 mb - размер чанка (меньше итераций оптимально)
    max_retries = 3  # если медленный интернет и провал по скорости загрузки

    file_path.parent.mkdir(exist_ok=True, parents=True)
    local_size = file_path.stat().st_size if file_path.exists() else 0

    # если это повторный запрос размеры кешированы в feedback_dict
    # тогда не нужно стучаться на сервер для получения заголовка
    if feedback_dict[label]['total'] == 0:
        total_size = await get_total_size(session, url=url, timeout=60.0)
    else:
        total_size = feedback_dict[label]['total']

    # Первичная проверка sha256, чтобы не качать зря большие файлы (если уже продолжение загрузки)
    # сохраняет ключ в feedback_dict для того, чтобы не запрашивать sha_api при реконнектах (rate_limitting сервера), при докачках
    if primary_check_sha256 and sha256 is not None:
        if not special_dict.get('sha256', False):
            sha_check = Sha256Checker.hf_check_sha256(url=url, sha256=sha256)
            if not sha_check:
                raise DownloadErr.Sha256MismatchPrimary(f'sha256 не совпадает для url {url}')
            else:
                special_dict['sha256'] = True  # чтобы дергать api сервера

    headers = {}

    # если файл уже есть, и его размер равен размеру файла отдаваемого сервером
    if local_size and total_size > 0 and (total_size - local_size) <= tolerance:
        async with lock:
            feedback_dict[label]['progress'] = 100.0
            feedback_dict[label]['total'] = total_size
            feedback_dict[label]['downolad'] = local_size
        return True

    # если файл уже есть, но не докачан, создать заголовок докачки
    if local_size and total_size > local_size:
        headers = {'Range': f'bytes={local_size}-'}

    headers[
        'User-Agent'
    ] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

    download_bytes = 0
    async with session.get(url, headers=headers, max_field_size=16384) as response:
        if response.status == 206:
            mode = 'ab'
            download_bytes = local_size
        elif response.status == 200:
            mode = 'wb'
        else:
            raise DownloadErr.StatusError(f'Ошибка при загрузке файла {file_path}, status_code = {response.status}')

        with open(file=file_path, mode=mode) as f:
            retries = 0
            while True:
                if event.is_set():  # отмена
                    response.close()
                    raise DownloadErr.Break(f'Отменена загрузка файла {file_path}')

                try:
                    chunk = await asyncio.wait_for(response.content.read(chunksize), timeout=chunk_timeout)
                except asyncio.TimeoutError:
                    retries += 1
                    if retries >= max_retries:
                        raise DownloadErr.TimeoutError(f'Файл `{file_path}` не удалось загрузить (timeout)')
                    if event.is_set():
                        raise DownloadErr.Break(f'Отменена загрузка файла {file_path}')
                    await asyncio.sleep(2)
                    continue

                if not chunk:
                    if response.content.at_eof():
                        break  # конец файла
                    else:
                        raise DownloadErr.StatusError(f'Соединение оборвалось на {download_bytes}/{total_size}')

                retries = 0  # сброс при успехе
                download_bytes += len(chunk)
                if total_size > 0:
                    download_percent = round((download_bytes / total_size) * 100, 1)
                    # обновление информации в очереди (обратная связь)
                    async with lock:
                        feedback_dict[label]['progress'] = download_percent
                        feedback_dict[label]['total'] = total_size
                        feedback_dict[label]['downolad'] = file_path.stat().st_size

                f.write(chunk)
    async with lock:
        feedback_dict[label]['progress'] = 100.0
        feedback_dict[label]['total'] = total_size
        feedback_dict[label]['downolad'] = file_path.stat().st_size
        if sha256:
            sha256_from_down_file = calculate_sha256(file_path=file_path)
            # вторичная (основная) проверка sha256, каждый файл который скачивается в конце проходит проверку безопасности
            # если хеши не сойдутся удалить файл и вызвать исключение
            if sha256_from_down_file != sha256:
                os.remove('\\\\?\\' + str(file_path))
                raise DownloadErr.Sha256MismatchSecondary(
                    f'Вторичная проверка sha256 не сходятся, файл удален. Для url {url}'
                )
    return True


def calculate_sha256(file_path: Path) -> str:
    sha256_hash = hashlib.sha256()
    # Читаем файл кусками по 64 КБ
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(65536), b""):
            sha256_hash.update(byte_block)  # noqa
    return sha256_hash.hexdigest()


async def example():
    async def observer(feedback_dict_in: dict, event_in: asyncio.Event):
        while not event_in.is_set():
            await asyncio.sleep(0.1)
            row = " | ".join([f"{k} : {v}%" for k, v in feedback_dict_in.items()])
            print(f'\r{row}', end='')

    timeout = ClientTimeout(
        total=None,  # самое важное, нужно обязательно сбросить таймаут, иначе большие файлы умрут при скачивании
        connect=30,
        sock_read=30,
        sock_connect=30,
    )

    event = asyncio.Event()
    feedback_dict = {"gemma-3-1b-it-Q4_K_M.gguf": {'progress': 0.0, 'total': 0, 'downolad': 0}}
    special_dict = {'sha256': False}  # служебный словарь для внутренних процессов загрузчика
    # задание на загрузку файла
    async with aiohttp.ClientSession(timeout=timeout) as session:
        download_task = asyncio.create_task(
            download_file(
                session=session,
                url='https://huggingface.co/lmstudio-community/gemma-3-1b-it-GGUF/resolve/main/gemma-3-1b-it-Q4_K_M.gguf',
                file_path=Path() / 'resources' / 'models' / 'gemma-3-1b-it-Q4_K_M.gguf',
                label='gemma-3-1b-it-Q4_K_M.gguf',  # название которое будет отображаться в прогресс баре
                event=event,  # событие завершения загрузки (механизм отмены)
                feedback_dict=feedback_dict,
                special_dict=special_dict,
                sha256='8d78d9d059a7605c401c105e169e0b08e9f0edc603ceb842f1c4bbb834296d17',
            ),
        )

        try:
            # прерывание загрузки
            # await asyncio.sleep(4)
            # event.set()
            observer_task = asyncio.create_task(observer(feedback_dict_in=feedback_dict, event_in=event))
            await download_task
            event.set()  # для завершения обсервера
            await observer_task  # обязательно дождаться, чтобы отображалось 100%
        except DownloadErr.Break:
            pass


if __name__ == '__main__':
    asyncio.run(example())
