import re, tomllib, requests, subprocess
from pathlib import Path
from rich import print

__all__ = ['sync']


def git_url_parse(git_url: str) -> tuple[str, str] | tuple[None, None]:
    """
    Парсинг url репозитория (поддерживает https, и ssh)
    :param git_url: url репозитория
    :return: автор репозитория, название репозитория
    """
    # SSH
    ssh_match = re.search(r'git@github\.com:(?P<author>\w+)/(?P<repo>\w+)\.git', git_url)
    if ssh_match:
        return ssh_match.group('author'), ssh_match.group('repo')

    # HTTPS
    https_match = re.search(r'https://github\.com/(?P<author>\w+)/(?P<repo>\w+)', git_url)
    if https_match:
        return https_match.group('author'), https_match.group('repo')

    return None, None


def get_latest_commit_hash(author: str, repo: str, git_branch: str) -> str | None:
    """Получение хеша последнего коммита"""
    # если у клиента есть гит (авторизованные запросы)
    url = f'https://github.com/{author}/{repo}.git'
    res = subprocess.run(['git', 'ls-remote', url, git_branch], capture_output=True, check=False)
    if res.returncode == 0 and res.stdout:
        git_hash = res.stdout.split()[0].decode('utf-8')
        return git_hash

    # если у клиента нет гита (неавторизованные запросы, ограничение -> 60 раз в час)
    try:
        response = requests.get(f"https://api.github.com/repos/{author}/{repo}/commits/{git_branch}")
        return response.json()["sha"]
    except requests.ConnectionError:
        print('[red]Нет соединения с git.[/red]')
        return None
    except Exception as err:
        print(f'[red]При попытке получить последнюю версию коммита возникла ошибка: {err}[/red]')
        return None


def sync(
        root_dir: Path,
        git_url: str,
        git_branch: str = 'main',
        ignore_deps: list[str] | None = None,
        callback=None,
) -> None:
    """
    Обновление зависимостей проекта, надстройка над uv sync, но со спецификой обработки git репозиториев, решает проблему
    обновлений, пакетов вложенных в репозиторий. Можно расширить для обновления специфических зависимостей через callback
    :param ignore_deps: игнорируемые пакеты (например если какие то очень долго обновляются и нужно пропустить)
    :param root_dir: корневой каталог
    :param git_url: ссылка на git, например: git@github.com:Mike2024New/infrastructure2.git
    :param git_branch: ветка git, например: main
    :param callback: функция расширитель с дополнительной логикой (применена до uv sync)
    :return: None
    """
    ignore_deps = ignore_deps or []
    res = subprocess.run(['uv', '--version'], capture_output=True)
    if res.returncode != 0:
        print(f'[red]Отсутствует uv[/red]')
        return None

    root_toml_path = root_dir / 'pyproject.toml'
    if not root_toml_path.exists():
        print(f'[red]Не найден pyproject.toml в корневой директории.[/red]')
        return None

    author, repo = git_url_parse(git_url=git_url)
    if author is None or repo is None:
        print(f'[red]Ошибка парсинга git_url: {git_url}[/red]')
        return None

    # 1. чтение toml (нужно получить все dependencies)
    with open(root_toml_path, mode='r', encoding='utf8') as f:
        current_toml_data = tomllib.loads(f.read())

    # 2. Получение зависимостей из toml
    deps_list = current_toml_data['project']['dependencies']
    sources_dict = current_toml_data.get('tool', {}).get('uv', {}).get('sources', {})

    for dep in deps_list:
        if dep in ignore_deps:
            continue
        # обработка зависимостей завязанных на git
        if any(dep == src for src in sources_dict.keys()) or 'git' in dep:
            if not 'git' in sources_dict.get(dep, {}) and not 'git' in dep:
                continue
            latest_commit = get_latest_commit_hash(author=author, repo=repo, git_branch=git_branch)
            if latest_commit is None:
                print(f'[yellow]Не удалось обновить {dep}, не получен хеш коммита.[/yellow]')
                continue
            if dep in sources_dict:
                if sources_dict[dep]['rev'] == latest_commit:
                    continue

            dep = dep.split('@')[0] if 'git' in dep else dep

            print(f'[green]Обновление пакета {dep}[/green]')
            update_url = (
                f'{dep} @ '
                f'git+https://github.com/{author}/{repo}.git'
                f'@{latest_commit}#subdirectory=packages/{dep.replace('-', '_')}'
            )
            cmd = ['uv', 'add', update_url]
            res = subprocess.run(cmd, capture_output=True)
            if res.returncode != 0:
                print(f'Не удалось обновить `{dep}`, ошибка: {res.stderr}')

    # функция расширитель
    if callback is not None and callable(callback):
        callback()

    # в конце обязательно сделать uv sync, для удаленных пакетов
    cmd = ['uv', 'sync']
    subprocess.run(cmd)
    return None


if __name__ == '__main__':
    sync(
        root_dir=Path.cwd(),
        git_url='git@github.com:Mike2024New/infrastructure2.git',
        # git_url='https://github.com/Mike2024New/infrastructure2',
        git_branch='main',
        ignore_deps=[],
    )
