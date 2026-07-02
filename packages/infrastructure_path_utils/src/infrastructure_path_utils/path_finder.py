from pathlib import Path
import sys

__all__ = ['get_root_dir_path', 'get_parent_by_marker']


def get_root_dir_path(venv_dir_name: str = '.venv') -> Path:
    """
    Определение корневой директории проекта.
    Работает по 2 принципам:
    Если вызов идет из .exe (bin), то выдаст текущую директорию
    Если же из кода то:
        .venv в корне проекта.
    :return: Path -> корневой путь к директории проекта
    """

    # для .exe / bin
    exe_mode = getattr(sys, 'frozen', False)
    if exe_mode:
        return Path(sys.executable).parent

    # для .venv (разработка - код)
    executable = Path(sys.executable)
    for parent in executable.parents:
        if parent.name == venv_dir_name:
            return parent.parent

    # .venv не найден
    raise RuntimeError(
        f'\nОшибка определения ROOT директории проекта \n'
        f'Папка виртуального окружения называется не .venv \n'
        f'Либо проект создан не на базе виртуального окружения\n'
    )


def get_parent_by_marker(path: Path, marker: str) -> Path | None:
    """
    Поиск пути до заданной папки ограничения
    :param path: исходный путь
    :param marker: критерий поиска, например src, поддерживает * для поиска, например '*src', '*src*', 'src*'
    :return: Укороченный до маркера путь
    Пример использования:
    res = get_parent_by_marker(
        path=Path(
            r'S:/_projects/python/Infrastructure2/packages/infrastructure_builder/src/infrastructure_builder/main.py'),
        marker='packages',
    )
    # res -> S:/_projects/python/Infrastructure2/packages
    """
    while path.parent != path:
        path = path.parent
        if path.name == marker:
            return path

        elif marker.startswith('*') and marker.endswith('*'):  # *substring*
            if marker.strip('*') in path.name:
                return path
        elif marker.startswith('*'):  # *suffix
            if path.name.endswith(marker[1:]):
                return path
        elif marker.endswith('*'):  # prefix*
            if path.name.startswith(marker[:-1]):
                return path

    return None


if __name__ == '__main__':
    print(get_root_dir_path())
