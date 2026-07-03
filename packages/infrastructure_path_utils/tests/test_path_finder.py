import sys
from pathlib import Path
import tempfile
from infrastructure_path_utils import get_root_dir_path, get_parent_by_marker

"""
Запуск тестов из терминала:
pytest -v -s
"""


def test_get_root_dir_path_returns_correct_path_when_venv_exists(monkeypatch):
    """
    Проверка что находится root_dir при наличии .venv в корневом каталоге
    """
    with tempfile.TemporaryDirectory() as temp:
        temp_dir_path = Path(temp)
        temp_dir_path_venv = temp_dir_path / '.venv'
        temp_dir_path_venv.mkdir(exist_ok=True, parents=True)
        # подмена путей sys для тестирования через monkeypatch
        fake_python = temp_dir_path_venv / 'Scripts' / 'activate' / 'python.exe'
        fake_python.parent.mkdir(parents=True, exist_ok=True)
        fake_python.touch()  # создать пустой файл, чтобы путь существовал
        # момент подмены пути
        monkeypatch.setattr(sys, 'executable', str(fake_python))
        # 1. проверка что виртуальное окружение найдено
        root_path = get_root_dir_path(venv_dir_name='.venv')
        assert root_path == temp_dir_path, 'Тест вернул не корректный путь корневой директории'


def test_get_root_dir_path_returns_correct_path_when_custom_venv_name(monkeypatch):
    """
    Проверка что находится root_dir при наличии .venv в корневом каталоге
    """
    with tempfile.TemporaryDirectory() as temp:
        temp_dir_path = Path(temp)
        temp_dir_path_venv = temp_dir_path / 'my_venv'
        temp_dir_path_venv.mkdir(exist_ok=True, parents=True)
        # подмена путей sys для тестирования через monkeypatch
        fake_python = temp_dir_path_venv / 'Scripts' / 'activate' / 'python.exe'
        fake_python.parent.mkdir(parents=True, exist_ok=True)
        fake_python.touch()  # создать пустой файл, чтобы путь существовал
        # момент подмены пути
        monkeypatch.setattr(sys, 'executable', str(fake_python))
        # 1. проверка что виртуальное окружение найдено
        root_path = get_root_dir_path(venv_dir_name='my_venv')
        assert root_path == temp_dir_path, 'Тест вернул не корректный путь корневой директории'


def test_get_root_dir_path_returns_none_when_venv_not_found(monkeypatch):
    """
    Проверка что не находится root_dir если папка виртуального окружения не была названа .venv
    """
    with tempfile.TemporaryDirectory() as temp:
        temp_dir_path = Path(temp)
        temp_dir_path_venv = temp_dir_path / 'venv'  # намеренно папка названа не .venv
        temp_dir_path_venv.mkdir(exist_ok=True, parents=True)
        # подмена путей sys для тестирования через monkeypatch
        fake_python = temp_dir_path_venv / 'Scripts' / 'activate' / 'python.exe'
        fake_python.parent.mkdir(parents=True, exist_ok=True)
        fake_python.touch()  # создать пустой файл, чтобы путь существовал
        # момент подмены пути
        monkeypatch.setattr(sys, 'executable', str(fake_python))
        # 1. проверка что тест не вернет путь если .venv отсутствует в каталоге
        root_path = get_root_dir_path()
        assert root_path is None, 'Тест вернул путь который не существует'


def test_get_root_dir_path_returns_exe_dir_when_frozen_mode_enabled(monkeypatch) -> None:
    """
    Проверка что приложение в режиме .exe будет возвращать корневую папку (где находится сам исполняемый файл)
    """
    with tempfile.TemporaryDirectory() as temp:
        temp_dir_path = Path(temp)
        monkeypatch.setattr(sys, 'frozen', True, raising=False)  # показать что режим .exe
        fake_exe_path = temp_dir_path / 'app.exe'
        fake_exe_path.touch()
        monkeypatch.setattr(sys, 'executable', str(fake_exe_path))  # пробросить путь исполняемого пути в тест
        root_path = get_root_dir_path()
        assert root_path == temp_dir_path, 'Тест не показал не корректную папку приложения'


def test_get_parent_by_marker_returns_parent_when_exact_name_matches():
    """Проверяет, что функция возвращает родительскую папку при точном совпадении имени"""
    test_path = Path('/home/projects/web/app1')
    expected_path = Path('/home/projects/')
    result_path = get_parent_by_marker(path=test_path, marker='projects', depth=1)
    assert result_path == expected_path, 'тест вернул не верный путь'


def test_get_parent_by_marker_returns_parent_when_marker_has_prefix_wildcard():
    """Проверяет поиск по началу имени, например infrastructure_*"""
    test_path = Path('/home/infrastructure_http_client/src/infrastructure_http_client/module1')
    expected_path = Path('/home/infrastructure_http_client/src/infrastructure_http_client')
    result_path = get_parent_by_marker(path=test_path, marker='infrastructure_*', depth=1)
    assert result_path == expected_path, 'тест вернул не верный путь'


def test_get_parent_by_marker_returns_parent_when_marker_contains_substring():
    """Проверяет поиск по подстроке, например *_http_*"""
    test_path = Path('/home/infrastructure_http_client/src/infrastructure_http_client/module1')
    expected_path = Path('/home/infrastructure_http_client/src/infrastructure_http_client')
    result_path = get_parent_by_marker(path=test_path, marker='*_http_*', depth=1)
    assert result_path == expected_path, 'тест вернул не верный путь'


def test_get_parent_by_marker_returns_parent_when_marker_has_suffix_wildcard():
    """Проверяет поиск по окончанию имени, например *_http_client"""
    test_path = Path('/home/infrastructure_http_client/src/infrastructure_http_client/module1')
    expected_path = Path('/home/infrastructure_http_client/src/infrastructure_http_client')
    result_path = get_parent_by_marker(path=test_path, marker='*_http_client', depth=1)
    assert result_path == expected_path, 'тест вернул не верный путь'


def test_get_parent_by_marker_skips_matches_according_to_depth_parameter():
    """Проверяет, что параметр depth позволяет пропускать нужное количество совпадений"""
    test_path = Path('/home/infrastructure_http_client/src/infrastructure_http_client/module1')
    expected_path = Path('/home/infrastructure_http_client')
    result_path = get_parent_by_marker(path=test_path, marker='infrastructure_http_client', depth=2)
    assert result_path == expected_path, 'тест вернул не верный путь'