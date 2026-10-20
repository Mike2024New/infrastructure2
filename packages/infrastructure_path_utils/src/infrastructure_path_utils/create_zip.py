import zipfile
from pathlib import Path


def create_zip_func(
        source_dir: Path,
        target_zip: Path,
        archive_root_folder_name: str | None = None
) -> None:
    """
    Упаковка директории в zip-архив.
    :param source_dir: Папка, которую нужно заархивировать.
    :param target_zip: Путь к создаваемому zip-файлу (например, Path('archive.zip')).
    :param archive_root_folder_name: Имя корневой папки внутри архива.
                                     Если None, файлы лягут в корень архива (без папки).
    """
    if not source_dir.exists() or not source_dir.is_dir():
        raise FileNotFoundError(f"Исходная директория не найдена: {source_dir}")

    # Убедиться, что родительская папка для архива существует
    target_zip.parent.mkdir(parents=True, exist_ok=True)

    # Открыть архив для записи (режим 'w' перезапишет файл, если он есть)
    with zipfile.ZipFile(target_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Проходим по всем файлам и папкам внутри source_dir
        for file_path in source_dir.rglob('*'):
            if file_path.is_file():
                # Вычислить путь файла относительно исходной папки
                # (например, 'my_project/src/main.py' -> 'src/main.py')
                arcname = file_path.relative_to(source_dir)

                # Если задано имя корневой папки, добавить его в начало пути
                if archive_root_folder_name:
                    arcname = Path(archive_root_folder_name) / arcname

                # Записать файл в архив
                zipf.write(file_path, arcname)


if __name__ == '__main__':
    # пример
    from infrastructure_path_utils import get_root_dir_path

    root_dir = get_root_dir_path()

    create_zip_func(
        source_dir=root_dir / 'app',  # например сборка приложения app
        target_zip=root_dir / 'win_x86_64.zip',  # выходной архив
        archive_root_folder_name=None,  # чтобы внутри не создавалась папка
    )
