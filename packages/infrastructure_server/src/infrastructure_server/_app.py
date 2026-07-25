import os
from fastapi import FastAPI, APIRouter, status
from infrastructure_server._server import Server
from datetime import datetime

__all__ = ['server_factory', 'Server']


def server_factory(
        component,
        routers_list: list[APIRouter] | None = None,
        message_bus=None,
        app_name: str = '<unknow app>',
) -> Server:
    """
    Фабрика Fastapi - принимает на вход роутеры (APIRouter). Возвращает экземпляр server.
    :param component: приложение выполняющее полезную нагрузку
    :param routers_list: кастомные эндпоинты APIRouters
    :param message_bus: шина сообщений из модуля infrastructure_message_bus
    :param app_name: название приложения которое будет отображаться при запуске сервера
    :return: объект сервера с методами start/stop
    """

    app = FastAPI()
    system_routers = APIRouter(tags=['system'])
    routers_list = routers_list or []
    server = Server(application=app, message_bus=message_bus, app_name=app_name)

    @system_routers.get('/')
    @system_routers.get('/health/')
    @system_routers.get('/status/')
    def component_status():
        """
        Проверка состояния сервера.
        """
        return {
            'msg': 'Сервер запущен.',
            'timestamp': datetime.now().isoformat(),
        }

    @system_routers.get(
        '/shutdown/',
        response_model=dict[str, str],
        status_code=status.HTTP_200_OK,
        summary='Остановка сервера'
    )
    def shutdown():
        """Остановка сервера"""
        # сперва остановить компонент если он запущен
        component.stop()
        # остановить сервер
        server.stop()
        return {
            'msg': 'сервер остановлен.',
            'timestamp': datetime.now().isoformat(),
        }

    @system_routers.get('/pid/')
    def pid():
        """Получение процесс id текущего сервера (для случаев когда приложения отдельные .exe)"""
        return {'pid': os.getpid(), 'msg': 'process id запущенного сервера.'}

    # добавление роутеров приложения (роутеры отличаются по тегам)
    for router in routers_list:
        app.include_router(router)

    app.include_router(system_routers)
    return server
