from pathlib import Path
import zipfile, tarfile


def check_zip_integrity(path_archive: Path):
    """Проверка архива на целостность, вычисляет битые архивы (полезно для проверки загрузок)"""
    try:
        with zipfile.ZipFile(path_archive, 'r') as z:
            bad_file = z.testzip()
            if bad_file is not None:
                raise RuntimeError(f"Файл '{bad_file}' внутри архива повреждён")
            # Если testzip вернул None — архив цел
            return True
    except (zipfile.BadZipFile, OSError, EOFError) as err:
        raise RuntimeError(f"Архив {path_archive.name} повреждён или недокачан (не zip): {err}")


def check_tar_gz_integrity(path_archive: Path):
    """Проверка архива на целостность, вычисляет битые архивы (полезно для проверки загрузок)"""
    try:
        with tarfile.open(path_archive, 'r:gz') as tar:
            for member in tar.getmembers():
                # Если файл в архиве повреждён, extractfile выкинет ошибку при чтении
                f = tar.extractfile(member)
                if f is not None:
                    # Читаем по кусочкам, чтобы не загружать гигабайты в память
                    while f.read(1024 * 1024):  # 1 MB chunks
                        pass
                    f.close()
        return True
    except (tarfile.TarError, OSError, EOFError) as err:
        # TarError — битый заголовок, OSError/EOFError — обрыв данных
        raise RuntimeError(f"Архив {path_archive.name} повреждён: {err}")
