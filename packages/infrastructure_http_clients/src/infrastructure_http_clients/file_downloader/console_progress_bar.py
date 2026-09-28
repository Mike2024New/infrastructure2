import asyncio
from infrastructure_http_clients.file_downloader.downloader import DownloadFile


async def progress_console_render(downloader: DownloadFile, event: asyncio.Event(), separator: str = ';') -> None:
    """
    Выводит в консоль прогресс загрузки.
    Решено выдавать данные одной строкой вида "v5_5_ru.pt 100.00&;3_en.pt 100.00", так как это можно распарсить на
    конечном клиенте (например Popen потребитель), и вывести как это будет удобно. Либо через progress бар.
    :param separator: разделитель для загрузок, по умолчанию ;
    :param downloader: объект загрузки (обратная связь с download модулем)
    :param event: событие выхода - загрузка завершена
    """
    while not event.is_set():
        await asyncio.sleep(0.1)
        new_row = {}
        for dwn in downloader.register:
            # файл уже существует
            if downloader.register[dwn].is_exists:
                new_row[dwn] = '100.00'

            elif downloader.register[dwn].done:
                new_row[dwn] = '100.00'
            else:
                downloaded_mb = downloader.register[dwn].download_bytes
                total_mb = downloader.register[dwn].total_bytes
                if total_mb > 0:
                    percent = round((downloaded_mb / total_mb) * 100, 1)
                    new_row[dwn] = percent
        if new_row:
            row = [f'{key} {val}' for key, val in new_row.items()]
            row = separator.join(row)
            print(row, flush=True)
