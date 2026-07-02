from pathlib import Path
import sys

__all__ = ['get_root_dir_path']


def get_root_dir_path(venv_dir_name: str = '.venv') -> Path:
    """
    Определение корневой директории проекта.
    Работает по 2 принципам:
    Если вызов идет из .exe (bin), то выдаст текущую директорию
    Если же из кода то:
    .venv в корне проекта.
    Если эта папка называется по другому, то прописать прямой путь в shared/env
    :return: Path -> корневой путь к директории проекта
    """

    # для .exe / bin
    exe_mode = getattr(sys, 'frozen', False)
    if exe_mode:
        return Path(sys.executable)

    executable = Path(sys.executable).parent
    for parent in executable.parents:
        if parent.name == venv_dir_name:
            return parent.parent

    # .venv не найден
    raise RuntimeError(
        f'\nОшибка определения ROOT директории проекта \n'
        f'Папка виртуального окружения называется не .venv \n'
        f'Либо проект создан не на базе виртуального окружения\n'
    )


if __name__ == '__main__':
    print(get_root_dir_path())
