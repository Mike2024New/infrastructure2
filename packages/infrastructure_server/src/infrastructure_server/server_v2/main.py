import uvicorn
import os
from fastapi import FastAPI, APIRouter
from typing import Literal

temp_x = 100


# ================= Клас обёртка над uvicorn ===========================
class ServerV2:
    def __init__(
            self,
            application: FastAPI,
            app_name: str = '<unknow app>',
            callback_start=None,
            callback_end=None,
            callback_start_error=None,
    ):
        """
        Класс надстройка над uvicorn, отвечает за запуск и остановку сервера.
        :param application: экземепляр приложения Fastapi с эндпоинтами.
        :param app_name: название приложения
        :param callback_start: функция которая выполнится перед стартом сервера
        :param callback_end: функция которая выполнится после завершения работы сервера
        """
        self._application = application
        self._app_name = app_name
        self._server: uvicorn.Server | None = None
        self._callback_start = callback_start
        self._callback_end = callback_end
        self._callback_start_error = callback_start_error
        self.parameters = {}

    def start(
            self,
            host: str = 'localhost', port: int = 8000,
            log_level: Literal['debug', 'info', 'warning', 'error'] = 'warning',
    ) -> None:
        """Запуск сервера на заданном порту, с указанным уровнем логирования."""
        try:
            self.parameters = {'app_name': self._app_name, 'host': host, 'port': port, 'pid': os.getpid()}
            if self._callback_start is not None and callable(self._callback_start):
                self._callback_start(self.parameters)
            config = uvicorn.Config(app=self._application, host=host, port=port, log_level=log_level)
            self._server = uvicorn.Server(config=config)
            self._server.run()
        except Exception as err:
            if self._callback_start_error is not None and callable(self._callback_start_error):
                details = self.parameters.copy()
                details['err'] = str(err)
                self._callback_start_error(details)
            raise Exception(f'Server {self._app_name}, runned error: {err}')

    def stop(self):
        """Остановка сервера. (Для cli утилит или для эндпоинтов)."""
        if self._callback_end is not None and callable(self._callback_end):
            self._callback_end(self.parameters)
        self._server.should_exit = True


# ================= Фабрика сервера ===========================
def server_factory_v2(
        app_name: str = '<unknow app>',
        callback_start=None,
        callback_end=None,
        callback_start_error=None,
        routers_list: list[APIRouter] | None = None,
        api_shudtown: bool = False,
        api_pid: bool = False,
) -> ServerV2:
    """
    Простая фабрика сервера. Расчитана для создания внутренних серверов.
    :param routers_list: кастомные роутеры приложений.
    :param app_name: название сервера для отображения его в api
    :param callback_start: действие перед запуском сервера (например логирование)
    :param callback_end: действие после завершения работы сервера (например логирование)
    :param callback_start_error: действие в случае ошибки (например логирование)
    :param api_shudtown: http завершение работы сервера ! Не рекомендуется включать для публичных api серверов!
    :param api_pid: http получение текущего id процесса ! Не рекомендуется включать для публичных api серверов!
    :return: Объект сервера с методами start(port, log_level), stop.
    """
    app = FastAPI(title=app_name)
    system_routres = APIRouter(tags=['system'])
    routers_list = routers_list or []

    server = ServerV2(
        application=app,
        app_name=app_name,
        callback_start=callback_start,
        callback_end=callback_end,
        callback_start_error=callback_start_error,
    )

    # добавление системных api
    def health_api_register():
        @system_routres.get('/health/')
        def health():
            """Проверка что сервер запущен"""
            return {'message': f'Server {app_name} is running.'}

    def shutdown_api_register():
        @system_routres.get('/shutdown/')
        def shutdown():
            """Завершение работы сервера"""
            server.stop()
            return {'message': f'server {app_name} is shutting down...'}

    def pid_api_register():
        @system_routres.get('/pid/')
        def pid():
            """Получение процесс id текущего сервера"""
            return {'pid': os.getpid(), 'msg': 'process id of the running server.'}

    # добавление эндпоинтов
    health_api_register()

    if api_shudtown:
        shutdown_api_register()

    if api_pid:
        pid_api_register()

    # добавление пользовательских роутеров приложения
    for router in routers_list:
        app.include_router(router)

    app.include_router(system_routres)
    return server
