from infrastructure_server.server_v1 import server_factory, Server
from infrastructure_server.server_v2 import server_factory_v2, ServerV2

__all__ = [
    'server_factory', 'Server',  # фабрика для генерации приложений / объект сервер для типизации
    'server_factory_v2', 'ServerV2',  # фабрика для генерации приложений / объект сервер для типизации
]
