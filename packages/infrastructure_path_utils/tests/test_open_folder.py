import pytest
from pathlib import Path
from infrastructure_path_utils import open_folder


def test_open_folder_raises_error_for_file(tmp_path):
    """Проверка, что функция не открывает файл, а выбрасывает ошибку"""
    # Создать временный файл
    file_path = tmp_path / "test.txt"
    file_path.touch()

    with pytest.raises(NotADirectoryError):
        open_folder(file_path)


def test_open_folder_raises_error_for_nonexistent_path():
    """Проверка, что функция не пытается открыть несуществующий путь"""
    with pytest.raises(FileNotFoundError):
        open_folder(Path("/path/that/does/not/exist/123456789"))
