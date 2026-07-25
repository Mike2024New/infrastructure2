import socket
import uvicorn
from fastapi import FastAPI
from typing import Literal


def find_free_port(start_port=8000, max_attempts=100, host='127.0.0.1'):
    """Находит первый свободный порт, начиная с start_port"""
    for port in range(start_port, start_port + max_attempts):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind((host, port))
            sock.close()
            return port
        except OSError:
            continue
    raise RuntimeError(f"Не найден свободный порт в диапазоне {start_port}-{start_port + max_attempts - 1}")


class Server:
    """
    Управление сервером, запуск остановка
    на вход при создании подать приложение fastapi
    start(port) по умолчанию 8000
    stop() остановка из внешних приложений
    ---------------------------------------------
    В реализации backend (или в cli) нужно вызывать метод server.stop()
    """

    def __init__(self, application: FastAPI, message_bus=None, app_name: str = '<unknow app>'):
        """

        :param application: приложение fastapi с эндпоинтами
        :param message_bus: шина сообщений из модуля infrastructure_message_bus
        :param app_name: наименование приложения
        """
        self._app_name = app_name
        self._application = application
        self.message_bus = message_bus
        self._server = None

    def start(
            self,
            port: int = 8000,
            port_find_max_attempts: int = 10,
            log_level: Literal['debug', 'info', 'warning', 'error'] = 'warning',
    ) -> None:
        """

        :param port: стартовый порт (если он занят, то будет запуск на первом свободном начиная с текущего порта)
        :param port_find_max_attempts: Максимальное количество попыток поиска свободного порта (относительно port)
        :param log_level:
        :return:
        """
        try:
            host = 'localhost'
            port = find_free_port(start_port=port, max_attempts=port_find_max_attempts, host=host)
            config = uvicorn.Config(app=self._application, host=host, port=port, log_level=log_level)
            self._server = uvicorn.Server(config)
            if self.message_bus is not None:
                self.message_bus(
                    subcomponent=self._app_name,
                    level='start',
                    event='server start',
                    message=f'server start -> app_name: {self._app_name} port: {port} host: {host}',
                    data={'host': host, 'port': port, 'log_level': log_level},
                )

            self._server.run()  # работает до тех пор пока self.server.shoud_exit=False
            if self.message_bus is not None:
                self.message_bus(
                    subcomponent=self._app_name,
                    level='stop',
                    event='server stop',
                    message=f'server stop -> app_name: {self._app_name} port: {port} host: {host}',
                )
        except Exception as err:
            if self.message_bus is not None:
                self.message_bus(
                    subcomponent=self._app_name,
                    level='error',
                    message='Ошибка запуска сервера',
                    event='server is not running',
                    error=err,
                )

    def stop(self):
        self._server.should_exit = True
