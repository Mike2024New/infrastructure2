import asyncio, aiohttp
from aiohttp import ClientTimeout
from pathlib import Path
from infrastructure_http_clients.file_downloader_v2.downloader_get_total_size import get_total_size
from infrastructure_http_clients.file_downloader_v2.exceptions import DownloadErr


async def download_file(
        session: aiohttp.ClientSession, url: str, file_path: Path, label: str, event: asyncio.Event,
        feedback_dict: dict[str, float]
) -> bool:
    """
    Загрузка одного конкретного файла, с несколькими попытками на чанк в случае ошибки
    :param session:
    :param feedback_dict: словарь очередей
    :param label: название загружаемого файла, может не совпадать с file_path это просто шильдик для словаря в queue_feedback
    :param url: ссылка на файл, например: https://huggingface.co/Systran/faster-whisper-tiny/resolve/main/model.bin
    :param file_path: путь к файлу, для url, например (для url из примера выше): target_dir / model.bin
    :param event: событие остановки (event.is_set())
    :return: bool
    """
    lock = asyncio.Lock()
    tolerance = 1024 * 1024  # 1mb
    chunk_timeout = 10  # время на ожидание одного чанка
    chunksize = 16 * 1024  # 16 mb - размер чанка (меньше итераций оптимально)
    max_retries = 3  # если медленный интернет и провал по скорости загрузки

    file_path.parent.mkdir(exist_ok=True, parents=True)
    local_size = file_path.stat().st_size if file_path.exists() else 0
    total_size = await get_total_size(session, url=url, timeout=60.0)

    headers = {}

    # если файл уже есть, и его размер равен размеру файла отдаваемого сервером
    if local_size and (total_size - local_size) <= tolerance:
        async with lock:
            feedback_dict[label] = 100.0
        return True

    # если файл уже есть, но не докачан, создать заголовок докачки
    if local_size and total_size > local_size:
        headers = {'Range': f'bytes={local_size}-'}

    download_bytes = 0
    async with session.get(url, headers=headers) as response:
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
                        feedback_dict[label] = download_percent
                f.write(chunk)
    async with lock:
        feedback_dict[label] = 100.0
    return True


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
    feedback_dict = {'tiny/model.bin': 0}
    # задание на загрузку файла
    async with aiohttp.ClientSession(timeout=timeout) as session:
        download_task = asyncio.create_task(
            download_file(
                session=session,
                url='https://huggingface.co/Systran/faster-whisper-tiny/resolve/main/model.bin',
                file_path=Path() / 'models' / 'tiny' / 'model.bin',
                label='tiny/model.bin',  # название которое будет отображаться в прогресс баре
                event=event,  # событие завершения загрузки (механизм отмены)
                feedback_dict=feedback_dict,
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
