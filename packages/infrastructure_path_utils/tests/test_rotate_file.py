import json
import tempfile
from pathlib import Path
import pytest
from infrastructure_path_utils import rotate_file_by_size_decorator


def test_rotate_file_by_size_decorator_limits_number_of_files():
    """Проверка, что декоратор ограничивает количество файлов"""
    files_limit = 3
    max_size_mb = 0.01  # маленький размер, чтобы файлы быстро ротировались

    with tempfile.TemporaryDirectory() as temp_dir:
        log_dir = Path(temp_dir) / 'logs'
        log_dir.mkdir()
        log_file = log_dir / 'log.jsonl'

        # Декорирование функцию записи
        @rotate_file_by_size_decorator(
            max_size_mb=max_size_mb,
            max_files=files_limit,
            index_separator='~',
            path_key_name='file_path',
            disable=False
        )
        def write_log(file_path: Path, content: dict):
            with open(file_path, 'a', encoding='utf-8') as f:
                f.write(json.dumps(content) + '\n')

        # много данных, чтобы вызвать ротацию
        for i in range(2000):
            write_log(file_path=log_file, content={"msg": str(i)})

        # Проверка количества файлов
        log_files = list(log_dir.iterdir())
        assert len(log_files) == files_limit

        # Проверка, что все файлы имеют правильные имена
        for i in range(files_limit):
            expected_name = f'log~{i}.jsonl'
            assert any(f.name == expected_name for f in log_files), f"Файл {expected_name} не найден"


def test_rotate_file_by_size_decorator_does_not_rotate_when_disable_true():
    """Проверка, что при disable=True декоратор не ротирует файлы"""
    with tempfile.TemporaryDirectory() as temp_dir:
        log_dir = Path(temp_dir) / 'logs'
        log_dir.mkdir()
        log_file = log_dir / 'log.jsonl'

        @rotate_file_by_size_decorator(
            max_size_mb=0.01,
            max_files=3,
            disable=True  # ← отключение ротации
        )
        def write_log(file_path: Path, content: dict):
            with open(file_path, 'a', encoding='utf-8') as f:
                f.write(json.dumps(content) + '\n')

        for i in range(100):
            write_log(file_path=log_file, content={"msg": str(i)})

        # Проверка, что создан только один файл (без ротации)
        log_files = list(log_dir.iterdir())
        assert len(log_files) == 1
        assert log_files[0].name == 'log.jsonl'


def test_rotate_file_by_size_decorator_raises_error_if_path_key_name_missing():
    """Проверка, что декоратор выбрасывает ошибку, если в kwargs нет path_key_name"""

    @rotate_file_by_size_decorator(path_key_name='file_path')
    def write_log(**kwargs):
        pass  # Декоратор должен упасть до вызова этой функции

    with pytest.raises(RuntimeError, match="необходимо передать путь с ключом `file_path`"):
        write_log(some_other_param='value')
