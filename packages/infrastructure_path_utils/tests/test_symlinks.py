import platform
import tempfile
from pathlib import Path
from infrastructure_path_utils import create_symlink


def test_create_symlink_corrected_link_create():
    """
    Проверка, что junction (Windows) или symlink (Linux) создаётся корректно.
    Проверка, что ссылка появилась и файл внутри неё доступен.
    """
    with tempfile.TemporaryDirectory() as temp:
        root_path = Path(temp)

        # 1. Создание тестовых папок
        fake_resources_path = root_path / 'resources'
        fake_target_dir = root_path / 'releases'
        fake_resources_path.mkdir(parents=True, exist_ok=True)
        fake_target_dir.mkdir(parents=True, exist_ok=True)

        # 2. Создать файл в исходной папке
        fake_resources_path_file = fake_resources_path / 'file1.txt'
        fake_resources_path_file.touch()

        # 3. Создание симлинка
        create_symlink(
            source_directory=fake_resources_path,
            target_directory=fake_target_dir,
        )

        # 4. Проверка, что папка-ссылка существует
        symlink_path = fake_target_dir / 'resources'
        assert symlink_path.exists(), "Папка с символической ссылкой не была создана"

        # 5. Проверка, что файл внутри ссылки доступен
        linked_file = symlink_path / 'file1.txt'
        assert linked_file.exists(), "Файл в симлинке не виден"

        # 6. Проверка, что это действительно ссылка, а не копия
        if platform.system().lower() == 'windows':
            pass
        else:
            # На Linux проверка, что это символическая ссылка
            assert symlink_path.is_symlink(), "Объект не является символической ссылкой"
