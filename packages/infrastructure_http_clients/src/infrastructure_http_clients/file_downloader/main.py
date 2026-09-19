import aiohttp, asyncio
from pathlib import Path
from infrastructure_http_clients.file_downloader.downloader import DownloadFile
from infrastructure_http_clients.file_downloader.models import DownloadFileType
from infrastructure_http_clients.file_downloader.console_progress_bar import progress_console_render


async def file_downloader(
        download_list: list[DownloadFileType],
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


if __name__ == '__main__':
    async def main():
        # пример использования:
        download_list = [
            # DownloadFileType(
            #     url_list=[
            #         'https://models.silero.ai/models/tts/ru/v5_5_ru.pt',
            #     ],
            #     target_dir=Path.cwd() / 'models' / 'silero',
            #     filename='v5_5_ru.pt',
            #     replace=False,
            # ),
            DownloadFileType(
                url_list=[
                    'https://github.com/astral-sh/python-build-standalone/releases/download/20260825/cpython-3.12.14+20260825-x86_64-pc-windows-msvc-install_only.tar.gz',
                ],
                target_dir=Path.cwd() / 'models' / 'python',
                filename='cpython-3.12.14+20260825-x86_64-pc-windows-msvc-install_only.tar.gz',
                replace=False,
            ),
        ]
        await file_downloader(download_list=download_list, console_progress_bar=True)


    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
