import tarfile
from pathlib import Path


def check_tar_gz_integrity(path_archive):
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


if __name__ == '__main__':
    check_tar_gz_integrity(
        path_archive=Path(
            r'S:\_projects\python\srv_standart\srv_installer\temp\utils\python\cpython-3.12.14+20260825-x86_64-pc-windows-msvc-install_only.tar.gz'),
    )
