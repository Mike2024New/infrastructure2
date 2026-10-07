import os
import shutil, zipfile
from pathlib import Path


def extract_zip_func(file: Path, delete_archive: bool = True, del_root_folder: bool = True) -> None:
    """
    Распаковка zip архива.
    :param file: путь к zip архиву
    :param delete_archive: удалять архив?
    :param del_root_folder: удалить корневую папку сместившись в верх? (распаковать содержимое в file.parent)
    """
    if not file.exists():
        return

    # 1. Распаковка архива
    with zipfile.ZipFile(file, 'r') as zip_ref:
        zip_ref.extractall(file.parent)  # extractall кладёт в archive/archive/source
        names = zip_ref.namelist()
        root_folder = names[0].split('/')[0] if '/' in names[0] else None

    # удаление архива
    if delete_archive:
        os.remove('\\\\?\\' + str(file))

    # архив без корневой папки
    if root_folder is None:
        return

    # 2. Пути к вложенной папке архива (если есть)
    source = file.parent / root_folder  # archive/repo-hash
    target = file.parent  # archive

    if source.exists() and not any(source.iterdir()):
        source.rmdir()

    if not del_root_folder:
        return

    # 3. Перемещение архивов наверх
    for item in source.iterdir():

        # если файл уже существует (например был скачан ранее установщиком, то удалить его)
        target_item = target / item.name
        if target_item.exists():
            if target_item.is_dir():
                shutil.rmtree('\\\\?\\' + str(target_item))
            else:
                os.remove('\\\\?\\' + str(target_item))

        shutil.move('\\\\?\\' + str(item), '\\\\?\\' + str(target / item.name))

    # 4. Удаление пустой папки из под архива
    source.rmdir()
