from pathlib import Path
from dataclasses import dataclass


@dataclass
class Download:
    url_list: list[str]
    target_dir: Path
    label: str
    replace: bool = False

@dataclass
class DownloadFile:
    url_list: list[str]
    target_dir: Path
    filename: str
    replace: bool = False


@dataclass
class DownloadMonitor:
    download_bytes: float = 0.0
    total_bytes: float = 0.0
    done: bool = False
    is_exists: bool = False
