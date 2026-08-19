from pathlib import Path


def find_interpreter_by_root_dir(root_dir: Path, venv_dir_name: str = '.venv') -> Path | None:
    """Поиск интерпретатора относительно root проекта, кроссплатформенно, для linux и для windows"""
    candidates = [
        root_dir / venv_dir_name / 'Scripts' / 'python.exe',
        root_dir / venv_dir_name / 'bin' / 'python',
    ]  # может расширяться
    return next((p for p in candidates if p.exists()), None)


if __name__ == '__main__':
    from infrastructure_path_utils import get_root_dir_path

    # поиск пути к интерпретатору
    res = find_interpreter_by_root_dir(
        root_dir=get_root_dir_path()  # корневой каталог, текущего проекта
    )
    print(res)
