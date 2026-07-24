from infrastructure_cli_utils.main import get_cli_app, cli_command_execute, CliSettings

__all__ = [
    'get_cli_app',  # объект набора базовых переиспользуемых команд
    'cli_command_execute',  # выполнение команды с выводом ошибки (если она произошла)
    'CliSettings',  # включение отключение эндпоинтов
]
