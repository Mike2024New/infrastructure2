from infrastructure_server._app import server_factory

__all__ = [
    'server_factory',  # фабрика для генерации приложений
]

"""
# Пример компонента (полезного приложения которое запускается внутри сервера):

class Component:
    def __init__(self):
        self.is_running: bool = False

    def start(self):
        self.is_running = True

    def stop(self):
        self.is_running = False
"""
