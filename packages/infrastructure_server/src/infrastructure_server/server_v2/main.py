import os, uvicorn
from fastapi import FastAPI, APIRouter, Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Type, Protocol, AsyncGenerator, Literal, Callable, Any


# ================ протокол для создания обработчиков исключений ======
class ExceptionHandlersProtocol(Protocol):
    @staticmethod
    def register(app: FastAPI) -> None: ...


# ================= Клас обёртка над uvicorn ===========================
class ServerV2:
    def __init__(
            self,
            application: FastAPI,
            app_name: str = '<unknow app>',
            callback_start: Callable[[Any], None] = None,
            callback_end: Callable[[Any], None] = None,
            callback_start_error: Callable[[Any], None] = None,
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
# 🙈 функция слегка перегружена кодом, нужно в идеале выделить время и попилить на компоненты
def server_factory_v2(
        app_name: str = '<unknow app>',
        lifespan: Callable[[FastAPI], AsyncGenerator[None, None]] | None = None,
        callback_start: Callable[[Any], None] = None,
        callback_end: Callable[[Any], None] = None,
        callback_start_error: Callable[[Any], None] = None,
        middleware_err_enable: bool = True,
        middleware_err_callback: Callable[[str, Exception], None] = None,
        routers_list: list[APIRouter] | None = None,
        middlewares_list: list[tuple[Type[BaseHTTPMiddleware], dict]] | None = None,
        exception_handlers: ExceptionHandlersProtocol | None = None,
        api_shudtown: bool = False,
        api_pid: bool = False,
) -> ServerV2:
    """
    Простая фабрика сервера. Расчитана для создания внутренних серверов.:
    :param lifespan:
    :param exception_handlers: кастомные обработчики исключений передаются через класс ExceptionHandlers
    :param middleware_err_enable: подключение энпоинта обрабатывающего непредусмотренные ошибки (убирает трассировку и терминала)
    :param middleware_err_callback: действие в случае ошибки в middleware_err, применяется если middleware_err_enable
    :param routers_list: кастомные роутеры приложений.
    :param middlewares_list: добавление промежуточных слоёв (последовательность важно)
    :param app_name: название сервера для отображения его в api
    :param callback_start: действие перед запуском сервера (например логирование)
    :param callback_end: действие после завершения работы сервера (например логирование)
    :param callback_start_error: действие в случае ошибки (например логирование)а
    :param api_shudtown: http завершение работы сервера ! Не рекомендуется включать для публичных api серверов!
    :param api_pid: http получение текущего id процесса ! Не рекомендуется включать для публичных api серверов!
    :return: Объект сервера с методами start(port, log_level), stop.
    """

    app = FastAPI(title=app_name, lifespan=lifespan)

    # подключение промежуточного слоя для обработки ошибок.
    if middleware_err_enable:
        @app.middleware("http")
        async def global_exception_middleware(request: Request, call_next):
            try:
                return await call_next(request)
            except Exception as exc:
                if middleware_err_callback is not None and callable(middleware_err_callback):
                    middleware_err_callback(request.url.path, exc)

                return JSONResponse(
                    status_code=500,
                    content={
                        "error": "Внутренняя ошибка сервера",
                        "detail": str(exc),
                        "path": request.url.path
                    }
                )

    # Подключение кастомных обработчиков специфических исключений (например ValueError)
    if exception_handlers is not None:
        exception_handlers.register(app)

    system_routres = APIRouter(tags=['system'])
    routers_list = routers_list or []
    middlewares_list = middlewares_list or []

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

    # добавление промежуточных слоёв (с параметрами)
    for midleware, kwargs in middlewares_list:
        app.add_middleware(midleware, **kwargs)

    # добавление пользовательских роутеров приложения
    for router in routers_list:
        app.include_router(router)

    app.include_router(system_routres)
    return server
