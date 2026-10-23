import truststore

# Использовать системное хранилище сертификатов ОС (Windows/macOS/Linux),
# иначе на части систем падает SSL: CERTIFICATE_VERIFY_FAILED
truststore.inject_into_ssl()

from infrastructure_http_clients.file_downloader_v3.main import downolad_many_files
from infrastructure_http_clients.file_downloader_v3.shemas import DownloadTask
from infrastructure_http_clients.file_downloader_v3.utils import observer

__all__ = [
    'downolad_many_files',
    'DownloadTask',
    'observer',
]
