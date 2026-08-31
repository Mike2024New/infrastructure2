import asyncio
import time
from rich.live import Live
from rich.table import Table
from infrastructure_http_clients.file_downloader.downloader import DownloadFile


async def progress_console_render(downloader: DownloadFile, event: asyncio.Event()):
    with Live(refresh_per_second=10) as live:
        while not event.is_set():
            await asyncio.sleep(0.1)

            table = Table(box=None)
            table.add_column("загрузка компонентов")
            for dwn in downloader.register:
                if downloader.register[dwn].is_exists:
                    table.add_row(f"{dwn}", f"[green]Уже есть, загрузка не требуется.[/green]")
                elif downloader.register[dwn].done:
                    table.add_row(f"{dwn}", f"[green]100%[/green]")
                else:
                    downloaded_mb = downloader.register[dwn].download_bytes
                    total_mb = downloader.register[dwn].total_bytes
                    if total_mb > 0:
                        percent = round((downloaded_mb / total_mb) * 100, 1) if total_mb > 0 else 0
                        table.add_row(f"{dwn}", f"[yellow]{percent}%[/yellow]")
                    else:
                        spinner = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
                        idx = int(time.time() * 10) % len(spinner)
                        table.add_row(f"{dwn}", f"[cyan]{spinner[idx]}[/cyan]")
            live.update(table)
