import truststore

# Использовать системное хранилище сертификатов ОС (Windows/macOS/Linux),
# иначе на части систем падает SSL: CERTIFICATE_VERIFY_FAILED
truststore.inject_into_ssl()

from infrastructure_http_clients.downloader import Downloader
from infrastructure_http_clients.adapters import adpater_download_from_hf
from infrastructure_http_clients.utils import ServerProbe
from infrastructure_http_clients.file_downloader import file_downloader, Download, DownloadFileType

__all__ = [
    'Downloader',  # загрузчик
    'adpater_download_from_hf',  # адаптеры для загрузки
    'ServerProbe',  # помощник в отладке серверов (например ожидание когда сервер будет загружен)
    # обновленный универсальный асинхронный загрузчик
    'file_downloader', 'Download', 'DownloadFileType',
]
