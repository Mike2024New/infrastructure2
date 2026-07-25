import uvicorn
from fastapi import FastAPI
from typing import Literal


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
            log_level: Literal['debug', 'info', 'warning', 'error'] = 'warning',
    ) -> None:
        """

        :param port: стартовый порт (если он занят, то будет запуск на первом свободном начиная с текущего порта)
        :param log_level:
        :return:
        """
        try:
            host = 'localhost'
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
