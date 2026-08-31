import aiohttp, asyncio
from pathlib import Path
from infrastructure_http_clients.file_downloader.downloader import DownloadFile
from infrastructure_http_clients.file_downloader.models import Download
from infrastructure_http_clients.file_downloader.console_progress_bar import progress_console_render


async def file_downloader(
        download_list: list[Download],
        console_progress_bar: bool = True,
        timeout: float = 5.0,
        attempts: int = 3,
        tolerance: int = 1024 * 64,
        chunk_size: int = 8192
) -> None:
    """
    Загрузка файлов, с fallback на резервные url в случае необходимости.
    Принимает список заданий на url (см подробнее download_list).
    :param console_progress_bar: показать прогесс бар загрузок в консоли
    :param download_list: список заданий.
        :param timeout: время ожидания одного чанка загрузки (на случай медленных соединений)
        :param chunk_size: размер буфера загрузки в байтах (чем меньше тем меньше ест памяти, но больше итераций и нагрузки на ЦП), для очень больших файлов можно повысить.
        :param attempts: количество попыток на 1 url (на тот случай если соединение например не установилось)
        :param tolerance: допуск отклонения размера файла в кб. (например git_api и фактический размер уже загруженного файла отличаются)
    :return:
    """
    async with aiohttp.ClientSession() as session:
        downloader = DownloadFile(timeout=timeout, attempts=attempts, tolerance=tolerance, chunk_size=chunk_size)
        tasks = [downloader.download(session, download) for download in download_list]
        event_progress = asyncio.Event()
        # подключение прогресс-бара
        if console_progress_bar:
            progress_task = asyncio.create_task(
                progress_console_render(
                    downloader=downloader,
                    event=event_progress,
                )
            )
        # ожидание загрузок
        await asyncio.gather(*tasks)
        # остановка прогесс бара
        if console_progress_bar:
            event_progress.set()
            await progress_task


async def main():
    # пример использования:
    download_list = [
        # Download(
        #     url_list=[
        #         'https://github.com/git-for-windows/git/releases/download/v2.54.0.windows.1/MinGit-2.54.0-64-bit.zip',
        #     ],
        #     target_dir=Path.cwd() / 'models' / 'MinGit',
        #     label='MinGit-2.54.0-64-bit.zip',
        #     replace=False,
        # ),
        # Download(
        #     url_list=[
        #         'https://github.com/Mike2024New/Pyoffline2/archive/refs/heads/main.zip',
        #     ],
        #     target_dir=Path.cwd() / 'models' / 'Pyoffline2',
        #     label='Pyoffline2.zip',
        #     replace=False,
        # ),
        Download(
            url_list=[
                'https://huggingface.co/Systran/faster-whisper-tiny/resolve/main/model.bin',
            ],
            target_dir=Path.cwd() / 'models' / 'faster-whisper-tiny',
            label='faster-whisper-tiny/model.bin',
            replace=False,
        ),
        # Download(
        #     url_list=[
        #         'https://huggingface.co/Systran/faster-whisper-tiny/resolve/main/config.json',
        #     ],
        #     target_dir=Path.cwd() / 'models' / 'faster-whisper-tiny',
        #     label='faster-whisper-tiny/config.json',
        #     replace=False,
        # ),
        # Download(
        #     url_list=[
        #         'https://huggingface.co/Systran/faster-whisper-tiny/resolve/main/tokenizer.json',
        #     ],
        #     target_dir=Path.cwd() / 'models' / 'faster-whisper-tiny',
        #     label='faster-whisper-tiny/tokenizer.json',
        #     replace=False,
        # ),
        # Download(
        #     url_list=[
        #         'https://huggingface.co/Systran/faster-whisper-tiny/resolve/main/vocabulary.txt',
        #     ],
        #     target_dir=Path.cwd() / 'models' / 'faster-whisper-tiny',
        #     label='faster-whisper-tiny/vocabulary.txt',
        #     replace=False,
        # ),
        # Download(
        #     url_list=[
        #         'https://alphacephei.com/vosk/models/vosk-model-small-ru-0.22.zip',
        #         'https://github.com/Mike2024New/STT_OFFLINE/releases/download/v1.1.0/vosk-model-small-ru-0.22.zip',
        #     ],
        #     target_dir=Path.cwd() / 'models' / 'vosk-model-small-ru-0.22',
        #     label='vosk-model-small-ru-0.22',
        #     replace=False,
        # ),
    ]
    await file_downloader(download_list=download_list, console_progress_bar=True)


try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass
