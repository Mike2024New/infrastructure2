import tomllib
from pathlib import Path
import subprocess
from rich import print


def sync2(
        root_dir: Path,
        git_branch: str = 'main',
        ignore_deps: list[str] | None = None
) -> None:
    """
    Обновление зависимостей проекта, надстройка над uv sync, но со спецификой обработки git репозиториев, решает проблему
    обновлений (смотрит на хеши коммитов).
    Для работы этой функции требуется настроенное с git ssh соединение
    :param root_dir: папка с pyproject.toml
    :param git_branch: ветка на гите (по умолчанию main)
    :param ignore_deps: игнорируемые зависимости (которые не нужно обновлять)
    :return: None
    """
    print(f'[green]Обновление пакетов - это может занять некоторое время.[/green]')
    ignore_deps = ignore_deps or []
    root_toml_path = root_dir / 'pyproject.toml'

    # проверка наличия uv
    res = subprocess.run(['uv', '--version'], capture_output=True)
    if res.returncode != 0:
        print(f'[red]Отсутствует uv[/red]')
        return None

    # проверка что toml есть
    if not root_toml_path.exists():
        print(f'[red]Не найден pyproject.toml в корневой директории.[/red]')
        return None

    # чтение toml (нужно получить все dependencies)
    with open(root_toml_path, mode='r', encoding='utf8') as f:
        current_toml_data = tomllib.loads(f.read())

    # Получение зависимостей из toml
    deps_list = current_toml_data['project']['dependencies']
    sources_dict = current_toml_data.get('tool', {}).get('uv', {}).get('sources', {})
    reposytories = {}
    url_updates_list = []

    # обход списка зависимостей
    for dep in deps_list:
        if dep in ignore_deps:
            continue

        if not 'github.com' in dep and dep not in sources_dict:
            continue

        repo_name = None
        if 'github.com' in dep:
            """Зависимости которые не прописаны в uv.sources"""
            if '@' not in dep:
                print(f'[yellow]Не удалось определить формат git_url для {dep}[/yellow]')
                continue
            repo_name = dep.split('@')[0].strip()
            sources_dict[repo_name] = {
                'git': 'https' + dep.split('@')[1].strip().split('https')[-1],
                'subdirectory': dep.split('subdirectory=')[-1] if 'subdirectory=' in dep else '',
                'rev': None,
            }
        repo_name = repo_name if repo_name is not None else dep

        #     # получение rev последнего комита
        if sources_dict[repo_name]['git'] not in reposytories:
            cmd = ['git', 'ls-remote', sources_dict[repo_name]['git'], git_branch]
            res = subprocess.run(cmd, capture_output=True, check=False)
            if res.returncode == 0 and res.stdout:
                git_hash = res.stdout.split()[0].decode('utf-8')
                reposytories[sources_dict[repo_name]['git']] = git_hash
            else:
                print(f'[yellow]Не удалось получить commit hash, для {sources_dict[repo_name]['git']}[/yellow]')
                continue
        else:
            git_hash = reposytories[sources_dict[repo_name]['git']]

        url_update = f'{repo_name} @ git+{sources_dict[repo_name]["git"]}@{git_hash}'
        if sources_dict[repo_name].get("subdirectory") is not None:
            url_update += f'#subdirectory={sources_dict[repo_name]["subdirectory"]}'
        url_update = url_update.lower()

        # если хеши не были указаны явно, то нужно обновить url
        if sources_dict[repo_name]['rev'] is not None:
            if sources_dict[repo_name]['rev'] != git_hash:
                url_updates_list.append(url_update)
                print(f'[green]{dep} - будет обновлен.[/green]')
        else:  # когда хеши не указаны
            url_updates_list.append(url_update)
            print(f'[green]{dep} - будет обновлен.[/green]')

    if url_updates_list:
        cmd = ['uv', 'add', *url_updates_list]
        subprocess.run(cmd)
    cmd = ['uv', 'sync']
    subprocess.run(cmd)
    return None


if __name__ == '__main__':
    sync2(
        git_branch='main',
        root_dir=Path.cwd(),
    )
