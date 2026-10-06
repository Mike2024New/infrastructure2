import os
import shutil, tarfile
from pathlib import Path


def extract_tar_func(file: Path, delete_archive: bool = True, del_root_folder: bool = True) -> None:
    """
    Распаковка tar/tar.gz/tgz архива.
    :param file: путь к архиву
    :param delete_archive: удалять архив?
    :param del_root_folder: удалить корневую папку сместившись в верх? (распаковать содержимое в file.parent)
    """
    if not file.exists():
        return

    # 1. Распаковка архива ('r:*' автоопределение gz/bz2/xz)
    with tarfile.open(file, 'r:*') as tar_ref:
        tar_ref.extractall(file.parent, filter='data')  # filter='data' защита от path traversal
        names = tar_ref.getnames()
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

    if not source.exists():
        return

    if not del_root_folder:
        return

    # 3. Перемещение содержимого наверх
    for item in source.iterdir():
        shutil.move('\\\\?\\' + str(item), '\\\\?\\' + str(target / item.name))

    # 4. Удаление пустой папки из под архива
    if source.exists() and not any(source.iterdir()):
        source.rmdir()