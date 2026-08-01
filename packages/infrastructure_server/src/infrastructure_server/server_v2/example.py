import uuid
from datetime import datetime
import asyncio
from time import perf_counter
from infrastructure_server import server_factory_v2
from fastapi import FastAPI, APIRouter, Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

"""
Документация с примерами:

Фабрика server_factory_v2 выдает объект сервера, который имеет методы:
    start - запуск сервера, опционально можно указать порты, уровень логирования starlette
    stop - остановка сервера (для тех случаев когда остановка сервера выполняется не через http)
------------------------------------------------------------------------------------------------------
Сервер имеет базовые эндпоинты:
    /health/      - проверка состояния сервера (Обязательный)
    /pid/         - pid сервера, для принудительной остановки в случае отключения терминала  (опциональный)
    /shutdown/    - остановка сервера  (опциональный)
------------------------------------------------------------------------------------------------------
Сервер может быть расширен кастомными роутерами (маршрутами) и промежуточными слоями (middleware)
------------------------------------------------------------------------------------------------------
У сервера можно определить функции перед и после запуска (lifespan метод)
------------------------------------------------------------------------------------------------------
Также у сервера есть возможность передать callback_start, callback_end - не путать с lifespan, эти
функции имеют например доступ к настройкам порта (так как в lifespan через app, нельзя получить текущий порт).
Эти функции хорошо подойдут для логирования. А lifespan подойдет для загрузки/выгрузки ресурсов.
start_callback, callback_end - знают `host`, `port`, `pid`, `app_name`
------------------------------------------------------------------------------------------------------
Сервер имеет middleware перехватывающий системные ошибки, по умолчанию включен. 
Но может быть и отключен при необходимости (например для вывода трассировки в консоль).
------------------------------------------------------------------------------------------------------
См. примеры ниже.
"""


def example1():
    """
    Минимальный запуск сервера.
    - Создает сервер с базовыми эндпоинтами (/health/, /pid/, /shutdown/).
    - Запускает его на localhost:8000.
    - Остановка через /shutdown/.
    """
    server = server_factory_v2(
        app_name='main',
        api_pid=True,  # явное подключение api (получение pid)
        api_shudtown=True,  # явное подключение api (остановка сервера)
        callback_start=lambda details: print(f'server start, details: {details}'),
        callback_end=lambda details: print(f'server end, details: {details}'),
    )
    print(f'Сервер запущен. Остановить по url `http://localhost:8000/shutdown/`')
    server.start(host='localhost', port=8000, log_level='info')  # запуск сервера.


def example2():
    """
    Создание сервера и расширение его кастомными роутерами.
    """
    # создание роутера (сети маршрутов):
    demo_router = APIRouter(tags=['demo'], prefix='/demo')

    # создание маршутов в роутере:
    @demo_router.get('/')
    def demo():
        return {'msg': 'demo'}

    # создание сервера
    server = server_factory_v2(
        app_name='main',
        # добавление дополнительных эндпоинтов
        routers_list=[demo_router],
        # функция перед запуском сервера
        callback_start=lambda details: print(f'server start, details: {details}'),
        # функция которая выполнится если системная ошибка:
        middleware_err_callback=lambda url, err: print(f'url : `{url}`, err : {err}'),
        # функция которая выполнится если возникла ошибка при попытке запустить сервер:
        callback_start_error=lambda details: print(f'server runned error: {details}'),
        # функция которая выполнится после остановки сервера:
        callback_end=lambda details: print(f'server stop, details: {details}'),
        # получение PID сервера (не использовать для публичных api)
        api_pid=True,
        # возможность отключить сервер через http (не использовать для публичных api)
        api_shudtown=True,
    )

    # запуск сервера
    print(f'Сервер запущен. Остановить по url `http://localhost:8000/shutdown/`')
    server.start(host='localhost', port=8000, log_level='info')  # запуск сервера.


def example3():
    """
    Демонстрация работы err_middleware.
    """
    # создание роутера (сети маршрутов):
    demo_router = APIRouter(tags=['demo'], prefix='/demo')

    # создание маршутов в роутере:
    @demo_router.get('/')
    def demo():
        # специально сделана нелепая ошибка, чтобы увидеть как отработает middleware_err
        result = 3 / 0  # делить на ноль могут только монахи математики с чёрным поясом 6-го дана
        return {'msg': result}

    # создание сервера
    server = server_factory_v2(
        app_name='main',
        # добавление дополнительных эндпоинтов
        routers_list=[demo_router],
        # по умолчанию он включен, но его можно выключить, например для создания своего обработчика
        middleware_err_enable=True,
        # функция которая выполнится если системная ошибка:
        middleware_err_callback=lambda url, err: print(f'Возникла нелепая ошибка -> url : `{url}`, err : {err}'),
        # получение PID сервера (не использовать для публичных api)
        api_pid=True,
        # возможность отключить сервер через http (не использовать для публичных api)
        api_shudtown=True,
    )

    # запуск сервера
    print(f'Сервер запущен. Остановить по url `http://localhost:8000/shutdown/`')
    server.start(host='localhost', port=8000, log_level='info')  # запуск сервера.


def example4():
    """
    Добавление промежуточного слоя middleware
    """
    # создание роутера (сети маршрутов):
    demo_router = APIRouter(tags=['demo'], prefix='/demo')

    # создание маршутов в роутере:
    @demo_router.get('/')
    async def demo():
        await asyncio.sleep(1)  # иммитация задержки
        return {'msg': 'demo'}

    # создание своего промежуточного слоя
    class CustomMiddleware(BaseHTTPMiddleware):
        def __init__(self, app, demo_parameter: str):
            super().__init__(app)
            self.demo_parameter = demo_parameter

        async def dispatch(self, request: Request, call_next):
            try:
                # ========== полезная нагрузка до ==========
                request_id = str(uuid.uuid4())[:4]
                start_time = perf_counter()
                print({'req_id': request_id, 'url': request.url, 'timestamp': datetime.now(), 'timedelta': 0})
                # ========== проброс url пользователю (в этой точке клиент видит http страницу) ==========
                response = await call_next(request)
                # ========== полезная нагрузка после  ==========
                end_time = round(perf_counter() - start_time, 2)
                print({'req_id': request_id, 'url': request.url, 'timestamp': datetime.now(), 'timedelta': end_time})
                return response
            except Exception as exc:
                return JSONResponse(
                    status_code=500,
                    content={
                        "error": "Внутренняя ошибка сервера",
                        "detail": str(exc),
                        "path": request.url.path
                    }
                )

                # создание сервера

    # создание сервера
    server = server_factory_v2(
        app_name='main',
        # добавление дополнительных эндпоинтов
        routers_list=[demo_router],
        # Добавление промежуточного слоя с __init__ аргументами для него
        middlewares_list=[(CustomMiddleware, {'demo_parameter': 'demo_parameter'})],
        # функция перед запуском сервера
        callback_start=lambda details: print(f'server start, details: {details}'),
        # функция которая выполнится если системная ошибка:
        middleware_err_callback=lambda url, err: print(f'url : `{url}`, err : {err}'),
        # функция которая выполнится если возникла ошибка при попытке запустить сервер:
        callback_start_error=lambda details: print(f'server runned error: {details}'),
        # функция которая выполнится после остановки сервера:
        callback_end=lambda details: print(f'server stop, details: {details}'),
        # получение PID сервера (не использовать для публичных api)
        api_pid=True,
        # возможность отключить сервер через http (не использовать для публичных api)
        api_shudtown=True,
    )

    # запуск сервера
    print(f'Сервер запущен. Остановить по url `http://localhost:8000/shutdown/`')
    server.start(host='localhost', port=8000, log_level='info')  # запуск сервера.


def example5():
    """
    Создание кастомных обработчиков и проброс их в фабрику.
    Срабатывает только после err_middleware (он отслеживает системные ошибки сервера 500 но можно ловить их через
    кастомные обработчики ExceptionHandlers)
    """
    from infrastructure_server.server_v2.main import ExceptionHandlersProtocol

    # нужно создать класс на базе ExceptionHandlersProtocol, и у него в методе register прописать обработчики
    class ExceptionHandlers(ExceptionHandlersProtocol):
        @staticmethod
        def register(app: FastAPI):
            # обработчик ответственный за исключение ZeroDivisionError
            @app.exception_handler(ZeroDivisionError)
            async def exception_zero_divizion_error(request: Request, exc: Exception):
                error = f'Ошибка, делить на ноль могут только монахи математики 6 дана с чёрным поясом'
                print(error)
                return JSONResponse(
                    status_code=400,
                    content={'error': error, 'detail': str(exc), 'path': request.url.path}
                )

            # обработчик ответственный за исключение ValueError
            @app.exception_handler(ValueError)
            async def handle_value_error(request: Request, exc: ValueError):
                return JSONResponse(
                    status_code=400,
                    content={'error': 'ошибка входных данных', 'detail': str(exc), 'path': request.url.path}
                )

    # создание роутера (сети маршрутов):
    demo_router = APIRouter(tags=['demo'], prefix='/demo')

    # создание маршутов в роутере:
    @demo_router.get('/')
    def demo():
        # специально сделана нелепая ошибка, чтобы увидеть как отработает middleware_err
        result = 3 / 0  # делить на ноль могут только монахи математики с чёрным поясом 6-го дана
        return {'msg': result}

    # создание сервера
    server = server_factory_v2(
        app_name='main',
        routers_list=[demo_router],
        middleware_err_enable=True,
        exception_handlers=ExceptionHandlers(),  # регистрация кастомных обработчиков
        api_shudtown=True,
    )

    # запуск сервера
    print(f'Сервер запущен. Остановить по url `http://localhost:8000/shutdown/`')
    server.start(host='localhost', port=8000, log_level='info')  # запуск сервера.


def example6():
    """Демонстрация создания lifespan (обёртка над сервером)"""
    from contextlib import asynccontextmanager

    @asynccontextmanager
    async def lifespan(_application: FastAPI):
        print(f'START')  # действие до запуска сервера
        yield  # работа сервера всё это время
        print(f'STOP')  # действие после запуска сервера

    server = server_factory_v2(
        app_name='main',
        api_shudtown=True,
        lifespan=lifespan,  # проброс lifespan
    )
    print(f'Сервер запущен. Остановить по url `http://localhost:8000/shutdown/`')
    server.start(host='localhost', port=8000, log_level='info')  # запуск сервера.


if __name__ == '__main__':
    # example1()  # простой запуск сервера (для демонстрации)
    # example2()  # запуск сервера с кастомными роутерами (расширение бизнес логикой)
    # example3()  # демонстрация встроенного middleware_err (перехватчика ошибок)
    # example4()  # запуск сервера с кастомным middleware
    # example5()  # Создание кастомных обработчиков и проброс их в фабрику
    example6()  # работа с lifespan
