from pathlib import Path
import zipfile


def check_zip_integrity(path_archive):
    """Проверка архива на целостность, вычисляет битые архивы (полезно для проверки загрузок)"""
    try:
        with zipfile.ZipFile(path_archive, 'r') as z:
            bad_file = z.testzip()
            if bad_file is not None:
                raise RuntimeError(f"Файл '{bad_file}' внутри архива повреждён")
            # Если testzip вернул None — архив цел
            return True
    except zipfile.BadZipFile:
        raise RuntimeError(f"Архив {path_archive.name} повреждён или недокачан (не zip)")


if __name__ == '__main__':
    check_zip_integrity(
        path_archive=Path(r'S:\_projects\python\srv_standart\srv_installer\temp\utils\git\git_portable.zip')
    )
