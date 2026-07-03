import pytest
from infrastructure_path_utils import FlatJsonManager


@pytest.fixture(scope='module')
def main(tmp_path_factory):
    test_dir = tmp_path_factory.mktemp('app_data')
    file_path_json = test_dir / 'demo.json'
    pm = FlatJsonManager(json_file_path=file_path_json)
    yield pm  # в рамках этого контекста временная папка будет жить


def test_flat_json_manager_adds_key_value_pair(main):
    """Проверка, что метод add() сохраняет ключ и значение"""
    main.add(key='test_key', value='test_value')
    assert main.get('test_key') == 'test_value'


def test_flat_json_manager_get_returns_none_for_missing_key(main):
    """Проверка, что get() возвращает None для несуществующего ключа"""
    assert main.get('non_existent_key') is None


def test_flat_json_manager_get_returns_default_for_missing_key(main):
    """Проверка, что get() возвращает default значение, если оно передано"""
    assert main.get('non_existent_key', default='default_value') == 'default_value'


def test_flat_json_manager_data_returns_all_stored_values(main):
    """Проверка, что data() возвращает полный словарь со всеми данными"""
    main.add(key='key1', value='val1')
    main.add(key='key2', value='val2')
    data_dict = main.data()
    assert 'key1' in data_dict
    assert data_dict['key1'] == 'val1'
    assert 'key2' in data_dict
    assert data_dict['key2'] == 'val2'


def test_flat_json_manager_removes_existing_key(main):
    """Проверка, что remove() удаляет существующий ключ"""
    main.add(key='key_to_remove', value='some_value')
    main.remove('key_to_remove')
    assert 'key_to_remove' not in main.data()


def test_flat_json_manager_remove_does_not_raise_for_missing_key(main):
    """Проверка, что remove() не падает при удалении несуществующего ключа"""
    # В текущей реализации remove() ничего не делает, если ключа нет
    # Просто проверка, что исключение не выбрасывается
    main.remove('non_existent_key')  # Не должно упасть (я попросил об этом 🙏)


def test_flat_json_manager_persists_data_to_file(main):
    """
    Проверка, что данные сохраняются в файл и читаются обратно (если поверх создается новый экземпляр)
    """
    main.add(key='persistent_key', value='persistent_value')
    # Создание новый менеджер, указывая на тот же файл
    new_manager = FlatJsonManager(main._json_file_path)
    # Проверка, что данные сохранились
    assert new_manager.get('persistent_key') == 'persistent_value'
