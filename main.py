import uuid
from infrastructure_git_client import GitClient
from infrastructure_settings_manager import TomlManager
from infrastructure_path_utils import get_root_dir_path
from pathlib import Path
from datetime import datetime


def commit(increment: bool = True) -> None:
    """
    Отправка обновления на git, с изменением версий дочерних пакетов (те которые были изменены) и
    фиксацией этих изменений в истории главного readme.md.
    Обновленные пакеты вычисляются через git status.
    :param increment: Если версии не нужно обновлять (например поменялось просто описание)
    :return: None
    """
    root_dir = get_root_dir_path()

    git_client = GitClient(
        root_dir=Path.cwd(),
        git_url='git@github.com:Mike2024New/infrastructure2.git',
        branch='main',
    )

    # получение списка всех пакетов файлы в которых менялись
    changed_packages = git_client.get_changes_packages(marker='src')
    if not changed_packages and not git_client.is_project_modified():
        print(f'Изменений нет, не чего коммитить.')
        return

    # получение основной метаинформации о проекте
    meta_toml_manager = TomlManager(root_dir)
    meta_today = datetime.now().strftime("%d.%m.%Y")
    meta_commit_hash = str(uuid.uuid4())[:6]
    meta_readme_md = root_dir / 'README.md'

    if increment:
        meta_toml_manager.inc_version(minor_in=True)

    change_packages_versions = []

    for pack in changed_packages:
        pack_root_path = pack.parent
        toml_manager = TomlManager(pack_root_path)
        if increment:
            toml_manager.inc_version(minor_in=True)
        change_packages_versions.append(f"{pack_root_path.name}=={toml_manager.get_version()}")

    # если есть изменения то создавать блок со списком новшеств
    if change_packages_versions:
        history_details = (
            f"<details>\n"
            f"<summary>{meta_today} - v{meta_toml_manager.get_version()} - {meta_commit_hash}</summary>\n\n"
            f"- {'\n- '.join(change_packages_versions)}\n"
            f"\n</details>"
        )

        # чтение главного README.md

        with open(file=meta_readme_md, mode='r', encoding='utf-8') as f:
            content = f.read().splitlines()
            insert_indx = 0
            for i, row in enumerate(content):
                if row == '<div id="change-history">':
                    insert_indx = i + 1
            content.insert(insert_indx, history_details)
            content = '\n'.join(content)

        # запись изменений в главный README.md
        with open(file=meta_readme_md, mode='w', encoding='utf-8') as f:
            f.write(content)

    git_client.commit(commit_message=meta_commit_hash)
    print(f'Коммит успешно отправлен.')
    # print(123)


if __name__ == '__main__':
    commit(increment=True)
