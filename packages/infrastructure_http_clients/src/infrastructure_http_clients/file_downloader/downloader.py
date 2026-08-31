import asyncio

from infrastructure_http_clients.file_downloader.get_file_size import get_total_size
from infrastructure_http_clients.file_downloader.models import DownloadMonitor
from infrastructure_http_clients.file_downloader.models import DownloadFileType
import aiohttp


class DownloadFile:
    def __init__(
            self,
            timeout: float = 10,
            chunk_size: int = 8192,
            attempts: int = 2,
            tolerance: int = 1024 * 64
    ):
        """
        :param timeout: время ожидания одного чанка загрузки (на случай медленных соединений)
        :param chunk_size: размер буфера загрузки в байтах (чем меньше тем меньше ест памяти, но больше итераций и нагрузки на ЦП), для очень больших файлов можно повысить.
        :param attempts: количество попыток на 1 url (на тот случай если соединение например не установилось)
        :param tolerance: допуск отклонения размера файла в кб. (например git_api и фактический размер уже загруженного файла отличаются)
        """
        self._timeout = timeout
        self._chunk_size = chunk_size
        self._attempts = attempts
        self._tolerance = tolerance
        self.register: dict[str, DownloadMonitor] = {}

    async def _download_file(self, session: aiohttp.client.ClientSession, url: str, download: DownloadFileType) -> None:
        """Скачивание файла по конкретному url. Обновляет данные по очкам загрузки"""
        self.register[download.filename] = DownloadMonitor()

        # создание директории (если её ещё нет)
        download.target_dir.mkdir(parents=True, exist_ok=True)
        # путь под которым будет сохранен файл
        file_path = download.target_dir / url.split('/')[-1]

        # получение размера файла
        if self.register[download.filename].total_bytes <= 0:
            total_size = await get_total_size(session, url=url, timeout=self._timeout)
            self.register[download.filename].total_bytes = total_size

        # размер уже скачанного файла (докачка если файл отсутствует)
        local_size = file_path.stat().st_size if file_path.exists() else 0

        headers = {}
        # проверка что файл не был скачан ранее
        if file_path.exists:

            if (
                    not download.replace and local_size > 0 and
                    abs(local_size - self.register[download.filename].total_bytes) <= self._tolerance
            ):
                self.register[download.filename].is_exists = True
                return

            # если файл существует и известен его размер а также размер скачиваемого файла, то сравнить их
            if (
                    local_size and self.register[download.filename].total_bytes
                    and self.register[download.filename].total_bytes > local_size
            ):
                headers = {'Range': f'bytes={local_size}-'}

        async with session.get(url, headers=headers) as response:
            if response.status == 206:
                mode = 'ab'
                self.register[download.filename].download_bytes = local_size
            else:
                mode = 'wb'

            with open(file_path, mode) as f:
                while True:
                    try:
                        chunk = await asyncio.wait_for(response.content.read(self._chunk_size), timeout=self._timeout)
                        if not chunk:  # все чанки получены, на выход
                            break
                        self.register[download.filename].download_bytes += len(chunk)
                        f.write(chunk)
                    except asyncio.TimeoutError:
                        raise

            self.register[download.filename].done = True

    async def download(self, session: aiohttp.client.ClientSession, download: DownloadFileType):
        """Загрузка файлов, с учётом fallback url."""
        exit_for = False
        for url in download.url_list:
            for _ in range(self._attempts):
                try:
                    await self._download_file(session, url=url, download=download)
                    exit_for = True
                    break
                except asyncio.TimeoutError:  # время загрузки вышло?
                    continue
                except aiohttp.ClientConnectionError:
                    continue
                except Exception:
                    raise
            if exit_for:
                break
