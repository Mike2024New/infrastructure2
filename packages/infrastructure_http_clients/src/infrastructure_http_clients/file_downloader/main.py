import aiohttp, asyncio
from pathlib import Path
from infrastructure_http_clients.file_downloader.downloader import DownloadFile
from infrastructure_http_clients.file_downloader.models import DownloadFileType
from infrastructure_http_clients.file_downloader.console_progress_bar import progress_console_render
from infrastructure_http_clients.file_downloader.console_progress_bar import feedback_progress


def downloads_detector(downloads: list[DownloadFileType]):
    """
    Определитель для нескольких url в задании на загрузку, это много разных файлов в одну папку? Например:

        url_list=[
            'https://huggingface.co/Systran/faster-whisper-tiny/resolve/main/config.json',
            'https://huggingface.co/Systran/faster-whisper-tiny/resolve/main/tokenizer.json',
            'https://huggingface.co/Systran/faster-whisper-tiny/resolve/main/model.bin',
            'https://huggingface.co/Systran/faster-whisper-tiny/resolve/main/vocabulary.txt',
        ],

    Тогда downloads будет пересобран на несколько downloads, с указанием одной папки.

    Или же это fallback (запасная ссылка), например:
        url_list=[
            'https://alphacephei.com/vosk/models/vosk-model-small-ru-0.22.zip',
            'https://github.com/Mike2024New/STT_OFFLINE/releases/download/v1.1.0/vosk-model-small-ru-0.22.zip',
        ],

    Тогда всё останется в исходном состоянии
    """
    new_downloads = []
    for dwn in downloads:
        files = set()
        for url in dwn.url_list:
            files.add(url.split('/')[-1])
        if len(files) > 1:  # если это не повторяющиеся файлы, то это именно fallback ссылки
            for url in dwn.url_list:
                new_downloads.append(
                    DownloadFileType(
                        filename=f"{dwn.target_dir.name}/{url.split('/')[-1]}",
                        url_list=[url],
                        target_dir=dwn.target_dir,
                    )
                )
        else:
            new_downloads.append(dwn)
    return new_downloads


async def file_downloader(
        download_list: list[DownloadFileType],
        timeout: float = 60,
        attempts: int = 3,
        tolerance: int = 1024 * 64,
        chunk_size: int = 8192,
        console_progress_bar: bool = False,
        feedback_queue: asyncio.Queue | None = None,
) -> None:
    """
    Загрузка файлов, с fallback на резервные url в случае необходимости.
    Принимает список заданий на url (см подробнее download_list).
    :param download_list: список заданий.
    :param timeout: время ожидания одного чанка загрузки (на случай медленных соединений)
    :param chunk_size: размер буфера загрузки в байтах (чем меньше тем меньше ест памяти, но больше итераций и нагрузки на ЦП), для очень больших файлов можно повысить.
    :param attempts: количество попыток на 1 url (на тот случай если соединение например не установилось)
    :param tolerance: допуск отклонения размера файла в кб. (например git_api и фактический размер уже загруженного файла отличаются)
    :param console_progress_bar: показать прогесс бар загрузок в консоли
    :param feedback_queue: в очередь записывается информация по загрузкам в виде (название файла, размер файла в mb): {'gemma-3-1b-it-Q4_K_M.gguf': 0.0, 'gemma-3-4b-it-Q4_K_M.gguf': 0.0, 'v3_en.pt': 100.0}
    """

    download_list = downloads_detector(download_list)  # авто распределение цепочка файлов в одну папку или fallback url

    async with aiohttp.ClientSession() as session:
        downloader = DownloadFile(timeout=timeout, attempts=attempts, tolerance=tolerance, chunk_size=chunk_size)
        tasks = [downloader.download(session, download) for download in download_list]
        event_progress = asyncio.Event()

        # обратная связь, чтобы получать очки загрузки файлов
        if feedback_queue is not None:
            feedback_progress_task = asyncio.create_task(
                feedback_progress(
                    downloader=downloader,
                    event=event_progress,
                    queue=feedback_queue,
                )
            )
        # подключение прогресс-бара
        if console_progress_bar:
            console_progress_task = asyncio.create_task(
                progress_console_render(
                    downloader=downloader,
                    event=event_progress,
                )
            )
        # ожидание загрузок
        await asyncio.gather(*tasks)
        event_progress.set()  # остановить задачи следящие за прогрессом

        if console_progress_bar:
            await console_progress_task
        if feedback_queue is not None:
            await feedback_progress_task


if __name__ == '__main__':
    async def main():
        # пример использования:
        download_list = [
            DownloadFileType(
                url_list=[
                    'https://models.silero.ai/models/tts/ru/v5_5_ru.pt',
                ],
                target_dir=Path.cwd() / 'models' / 'silero',
                filename='v5_5_ru.pt',
                replace=False,
            ),
            # DownloadFileType(
            #     url_list=[
            #         'https://github.com/astral-sh/python-build-standalone/releases/download/20260825/cpython-3.12.14+20260825-x86_64-pc-windows-msvc-install_only.tar.gz',
            #     ],
            #     target_dir=Path.cwd() / 'models' / 'python',
            #     filename='cpython-3.12.14+20260825-x86_64-pc-windows-msvc-install_only.tar.gz',
            #     replace=False,
            # ),
            # DownloadFileType(
            #     url_list=[
            #         'https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip',
            #         'https://github.com/Mike2024New/STT_OFFLINE/releases/download/v1.1.0/vosk-model-small-en-us-0.15.zip',
            #     ],
            #     target_dir=Path.cwd() / 'models' / 'vosk',
            #     filename='vosk-model-small-en-us-0.15.zip',
            #     replace=False,
            # ),
        ]
        await file_downloader(download_list=download_list, console_progress_bar=False)


    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
