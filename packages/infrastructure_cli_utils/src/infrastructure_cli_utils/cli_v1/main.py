import typer, subprocess
from rich import print
from pathlib import Path
from typing import Callable, Any, Literal
from infrastructure_builder import BuildParameters
from infrastructure_builder import build as builder_func
from infrastructure_git_client import adapter_git_push_update
from infrastructure_path_utils.open_folder import open_folder
from infrastructure_other import parse_value_and_type_from_string
from infrastructure_other import sync as uv_sync
from dataclasses import dataclass
from typing import Protocol

"""
Шаблон для микросервисов
"""


class ServerV1(Protocol):
    # класс для типизации сервера
    def start(self, port: int, log_level: Literal['debug', 'info', 'warning', 'error']): ...

    def stop(self): ...


class ServerV2(Protocol):
    # класс для типизации сервера
    def start(self, host: str, port: int, log_level: Literal['debug', 'info', 'warning', 'error']): ...

    def stop(self): ...


@dataclass
class CliSettings:
    enable_run_command: bool = False
    enable_run_server: bool = False
    enable_folder_command: bool = True
    enable_build_command: bool = False
    enable_git_push: bool = False
    enable_run_test: bool = False
    enable_settings_show: bool = False
    enable_settings_edit: bool = False
    enable_register_sync: bool = False


_exe_mode: bool = False
_message_bus: Any | None = None

__all__ = [
    'get_cli_app',  # объект набора базовых переиспользуемых команд
    'cli_command_execute',  # выполнение команды с выводом ошибки (если она произошла)
    'CliSettings',  # включение отключение эндпоинтов
]


def cli_command_execute(callback: Callable, command_name: str) -> Any | None:
    """
    Обработка команды, с отловом ошибки
    :param callback: исполняемая функция с аргументами
    :param command_name: Название команды app.info.name
    :return: результат выполнения функции либо None
    """
    try:
        return callback()
    except Exception as err:
        if _message_bus is not None:  # логирование ошибки
            _message_bus(
                level='error',
                subcomponent='cli',
                message=f'Ошибка в процессе выполнения команды {command_name}',
                event='cli run command error',
                error=err,
            )

        if _exe_mode:  # для exe режима
            print(f'[red]Ошибка в процессе выполнения команды: {err}[/red]')
        else:  # для разработчиков
            raise
    return None


def create_cli_app(name: str) -> typer.Typer:
    app = typer.Typer(
        name=name,
        no_args_is_help=True,
        # если пользователь дал команду без аргументов то не падать с ошибкой а показать справку
        rich_markup_mode='rich',
        # добавить rich панели (группировка комманд по заголовкам)
        add_completion=False,  # убрать блок option в всплывающем меню
        invoke_without_command=True,  # разрешить запуск без команд
    )

    @app.callback()
    def main():
        """CLI интерфейс"""

    return app


def register_run_server(
        app: typer.Typer,
        server: ServerV1 | ServerV2,
        trace_id_callback: Callable[[str], ...] | None = None,
):
    @app.command()
    def run_server(
            ctx: typer.Context,
            port: int = typer.Option(8000, '--port', '-p'),
            log_level: Literal['debug', 'info', 'warning', 'error'] = typer.Option('warning', '--log-level', '-ll'),
            trace_id: str = typer.Option(None, '-ti', '--trace-id'),
    ):
        """
        Запуск сервера с полезной нагрузкой.
        Сервер имеет базовые эндпоинты:
            [green]/health/[/green]      - проверка состояния сервера
            [green]/parameters/[/green]  - параметры текущего компонента
            [green]/pid/[/green]         - pid сервера, для принудительной остановки в случае отключения терминала
            [green]/shutdown/[/green]    - штатное завершение работы сервера
        Опции:
            -p (--port)         - порт на котором будет запущен сервер (по умолчанию 8000)
            -ll (--log-level)   - минимальный уровень логирования ('debug', 'info', 'warning', 'error')
            -ti (--trace-id)    - id сквозной трассировки - для отслеживания цепочки логов нескольких компонентов
        Примеры команд:
            [yellow]run-server[/yellow]            - с параметрами по умолчанию
            [yellow]run-server -p 8000[/yellow]    - с указанием порта
            [yellow]run-server -ll info[/yellow]   - с минимальным уровнем логирования info
            [yellow]run-server -ti #000[/yellow]   - с передачей id цепочки операций
        """
        # в этой точке можно добавить ключ трассировки цепочки операций (для разных компонентов)
        if trace_id is not None and trace_id_callback is not None:
            cli_command_execute(
                lambda: trace_id_callback(trace_id),
                command_name=ctx.command.name,
            )
        elif trace_id is not None and trace_id_callback is None:
            print('[yellow]trace_id не обработан, для неё нужно передать trace_id_callback, в cli_settings[/yellow]')

        cli_command_execute(
            lambda: server.start(port=port, log_level=log_level),
            command_name=ctx.command.name,
        )
        return


def register_settings_show(app: typer.Typer, settings):
    @app.command()
    def settings_show(ctx: typer.Context):
        """
        Просмотр текущих настроек
        Примеры команд:
            [yellow]settings-show[/yellow]
        """
        cli_command_execute(
            callback=lambda: print(settings),
            command_name=ctx.command.name,
        )


def register_settings_edit(app: typer.Typer, settings, settings_manager):
    @app.command()
    def settings_edit(ctx: typer.Context, params: list[str] = typer.Argument(None)):
        """
        Обновление настроек (работает для плоской архитектуры ключ-значение)
        Парсит значения из строк (например 512 будет определено как int, что корректно для моделей pydantic)
        Примеры команд:
            [yellow]settings-edit samplerate=32000 blocksize=512 name=test[/yellow]
        """

        def edit_parameters():
            if params is None:
                print(f'[red]Нужно передать хотябы одну пару параметров.[/red]')
                return
            for par in params:
                if '=' not in par or par.count('=') > 1:
                    raise RuntimeError(f'Не корректно введены параметры {params}')
                key, val = par.split('=')
                val = parse_value_and_type_from_string(val)[0]

                if hasattr(settings, key):
                    setattr(settings, key, val)

            settings_manager.apply_new_settings(settings=settings)

        cli_command_execute(
            callback=lambda: edit_parameters(),
            command_name=ctx.command.name,
        )


def register_run_command(app: typer.Typer):
    @app.command()
    def run(ctx: typer.Context):
        """[red][bold]Нужно переопределить этот метод в приложении![/bold][/red]"""
        cli_command_execute(
            callback=lambda: print(
                f'[yellow]Команда не переопределена, главный метод приложения должен называться run[/yellow]'
            ),
            command_name=ctx.command.name,
        )


def register_folder_command(app: typer.Typer, root_dir: Path) -> None:
    @app.command()
    def folder(ctx: typer.Context):
        """Открыть домашнюю папку приложения"""
        cli_command_execute(
            callback=lambda: open_folder(root_dir),
            command_name=ctx.command.name,
        )


def register_build_command(app: typer.Typer, build_settings: BuildParameters) -> None:
    @app.command()
    def build(
            ctx: typer.Context,
            name: str | None = typer.Option(None, '-n', '-name'),
            one_file: bool = typer.Option(False, '-oe', '--onefile', flag_value=True),
            entry_path: Path | None = typer.Option(None, '-ep', '--entry_path'),
            create_resources_symlink: bool = typer.Option(False, '-sl', '--sym-link', flag_value=True),
            copy_to_target: Path = typer.Option(None, '-ct', '--copy-to-target'),
    ):
        """
        [red]~dev [/red]Создание сборки, приложения .exe или .bin [yellow]build[/yellow]
        система определяется автоматически windows/linux
        Опции:
            -n (--name) - название приложения (если не переопределить то взьмется по умолчанию из settings)
            -oe (--onefile) - сборка одним файлом (по умолчанию выключена)
            -sl (--sym-link) - создать симлинк на папку с ресурсами
            -ep (--entry-path) - стартовый скрипт (по умолчанию этот же скрипт cli_utils.py)
            -ct (--copy-to-target) - Путь куда копировать сборку из dist в заданную папку (например на рабочий стол)
        Примеры команд:
            [yellow]build[/yellow]
            [yellow]build -n my-app[/yellow] - указать название приложения
            [yellow]build -oe[/yellow] - сборка одним файлом
            [yellow]build -ep ./main.py[/yellow] - входная точка приложения указанный файл
            [yellow]build -sl[/yellow] - создать симлинк на папку с ресурсами (для разработки)
            [yellow]build -n my-app -oe -ep -s ./main.py[/yellow] - все вместе с указанием точки сборки
        """

        # переопределение опций
        # build_settings = build_settings or BuildParameters()
        build_settings.name = name if name is not None else build_settings.name
        build_settings.one_file = one_file
        build_settings.create_resources_symlink = create_resources_symlink
        build_settings.entry_point_path = entry_path if entry_path is not None else build_settings.entry_point_path
        build_settings.copy_from_dist_to_target_dir = copy_to_target if copy_to_target is not None else build_settings.copy_from_dist_to_target_dir

        cli_command_execute(
            callback=lambda: builder_func(build_settings),
            command_name=ctx.command.name,
        )


def register_git_push(app: typer.Typer, root_dir: Path):
    @app.command()
    def git_push(
            ctx: typer.Context,
            notests: bool = typer.Option(False, '-nt', '--notests', flag_value=True),
    ):
        """
        [red]~dev [/red]Отправка git, с редактированием минорной версии в pyproject.toml, и редактировании блока
        истории в .md (при условии что там есть заголовок [yellow]`## История развития модуля`[/yellow] и в нем написана новость
        вида [yellow]`@new`[/yellow]. В корне проекта должен быть файл .env с переменными GIT_URL=<ваш url>, GIT_BRANCH=<ветка>.
        Перед коммитом запускаются тесты, если тесты не пройдены, коммит отменяется.
        Опции:
            -nt (--notests) - не делать тесты перед коммитом

        Примеры команд:
            [yellow]git-push[/yellow]
            [yellow]git-push -nt[/yellow] - коммит без тестов
        """

        # выполнить тесты перед коммитом
        if not notests:
            result: subprocess.CompletedProcess = cli_command_execute(
                callback=lambda: subprocess.run(['pytest', '-v', '-s'], cwd=root_dir),
                command_name=ctx.command.name,
            )
            if result and result.returncode != 0:
                print('[red]Коммит отменён — тесты не пройдены[/red]')
                return

        adapter_git_push_update(
            root_dir=root_dir,
            history_header='## История развития модуля',
            history_new_marker='@new',
        )


def register_sync(app: typer.Typer, root_dir: Path):
    @app.command()
    def sync(ctx: typer.Context, ignore_deps: str | None = typer.Option(None, '-id', '--ignore-deps')):
        """
        [red]~dev [/red]Обновить пакеты из pyproject.toml, корректно обновляет вложенные репозитории с git.
        Опции:
            -id (--ignore-deps) - игнорировать пакеты, перадать аргумены в кавычках
        Примеры команд:
            [yellow]sync[/yellow]
            [yellow]sync -id "infrastructure-server"[/yellow] - обновить все пакеты кроме infrastructure-server
        """
        cli_command_execute(
            lambda: uv_sync(
                root_dir=root_dir,
                git_url='https://github.com/Mike2024New/infrastructure2',
                git_branch='main',
                ignore_deps=ignore_deps.split() if ignore_deps is not None else [],
            ),
            command_name=ctx.command.name,
        )


def register_run_test(app: typer.Typer, root_dir: Path):
    @app.command()
    def run_tests(
            ctx: typer.Context,
            v: bool = typer.Option(False, '-v', flag_value=True),
            s: bool = typer.Option(False, '-s', flag_value=True),
    ):
        """
        [red]~dev [/red]Запуск тестов.
        Опции:
            -v - подробный режим с путем к каждому модулю
            -s - показывать принты внутри тестов
        Примеры команд:
            [yellow]run-tests -v -s[/yellow] - запуск тестов
        """
        cmd = ['pytest']

        # # добавление опций / add options
        cmd.extend(['-v']) if v else cmd.extend([])
        cmd.extend(['-s']) if s else cmd.extend([])

        result: subprocess.CompletedProcess = cli_command_execute(
            callback=lambda: subprocess.run(cmd, cwd=root_dir),
            command_name=ctx.command.name,
        )
        if result and result.returncode != 0:
            print('[red]Тесты не пройдены.[/red]')


def get_cli_app(
        name: str,
        root_dir: Path,
        build_settings: BuildParameters | None = None,
        exe_mode: bool = False,
        message_bus=None,
        cli_settings: CliSettings | None = None,
        settings: Any = None,
        settings_manager: Any = None,
        server: ServerV1 | ServerV2 | None = None,
        trace_id_callback: Callable[[str], ...] | None = None,
) -> typer.Typer:
    """
    Получение экземпляра typer для консоли приложения, с предопределенными базовыми методами.
    :param trace_id_callback: функция обработчик trace_id, например модификация id в шине сообщений (модуль infrastructure2/message_bus)
    :param cli_settings: настройки какие команды будут отображаться в cli.py по умолчанию все
    :param name: название приложения
    :param root_dir: корневая папка проекта
    :param build_settings: настройки для сборщика (передавать не обязательно, возьмутся опциональные параметры)
    :param exe_mode: режим exe (приложение) или разработка?
    :param message_bus: Опционально: шина сообщений (см. подробнее `message_bus_factory_v2` в модуле infrastructure.message_bus)
    :param settings_manager: (объект get_settings_manager из пакета infrastructure_settings_manager)
    :param settings: (объект settings из пакета сформированный из модели schemas проекта)
    :param server: (объект Server из пакета infrastructure_server (имеет метод server.start(port, log-level)))
    :return: экземпляр приложения. Который запускается app()
    Пример использования:

    # =========== cli_utils.py =============================================================
    import config
    from cli_base.cli_base import get_cli_app

    # получение базовых повторяющихся команд
    app = get_cli_app(
        name='llm',
        root_dir=config.ROOT_DIR, # корневая папка проекта (в которой лежат pyproject.toml, *.md файлы)
        exe_mode=config.EXE_MODE, # режим работы (код/сборка),
    )

    # запуск:
    if __name__ == '__main__':
        app()
    # =================================================================================
    """
    global _exe_mode, _message_bus

    cli_settings = cli_settings or CliSettings()

    app = create_cli_app(name=name)
    _exe_mode = exe_mode
    _message_bus = message_bus
    # общие команды
    if cli_settings.enable_run_command:
        register_run_command(app=app)  # переопределяемый в дочках метод

    # октрывать корневую директорию проекта
    if cli_settings.enable_folder_command:
        register_folder_command(app=app, root_dir=root_dir)

    # команда просмотра настроек
    if cli_settings.enable_settings_show:
        if settings is None:
            raise RuntimeError(
                f'Не передан объект settings для формирования cli команды settings-show'
            )
        register_settings_show(app=app, settings=settings)

    # команда редактирования настроек
    if cli_settings.enable_settings_edit:
        if settings is None or settings_manager is None:
            raise RuntimeError(
                f'Не переданы объекты settings, settings_manager, для формирования cli команды settings-edit'
            )
        register_settings_edit(app=app, settings=settings, settings_manager=settings_manager)

    # команда подключения сервера
    if cli_settings.enable_run_server:
        if server is None:
            raise RuntimeError(
                f'Для формирования команды run-server необходимо передать объект server.'
            )
        register_run_server(app=app, server=server, trace_id_callback=trace_id_callback)

    if not exe_mode:  # команды которые будут доступны только в режиме разработчика
        if cli_settings.enable_run_test:
            register_run_test(app=app, root_dir=root_dir)
        if cli_settings.enable_git_push:
            register_git_push(app=app, root_dir=root_dir)
        if cli_settings.enable_build_command:
            build_settings = build_settings or BuildParameters()  # проброс настроек
            register_build_command(app=app, build_settings=build_settings)
        if cli_settings.enable_register_sync:
            register_sync(app=app, root_dir=root_dir)
    return app
