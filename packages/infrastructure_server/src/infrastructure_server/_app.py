from fastapi import FastAPI, APIRouter, status
from infrastructure_server._server import Server
from datetime import datetime


def server_factory(component, routers_list: list[APIRouter] | None = None, message_bus=None) -> Server:
    """
    Фабрика Fastapi - принимает на вход роутеры (APIRouter). Возвращает экземпляр server.
    """

    app = FastAPI()
    system_routers = APIRouter(tags=['system'])
    routers_list = routers_list or []
    server = Server(application=app, message_bus=message_bus)

    @system_routers.get('/')
    @system_routers.get('/health/')
    @system_routers.get('/status/')
    def component_status():
        """
        Проверка состояния сервера. Проверка запущен ли компонент сервера (component_is_run).
        """
        return {
            'msg': 'Основная информация о сервере.',
            'component_is_run': component.is_running,
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
            'msg': 'сервер остановлен.'
        }

    # добавление роутеров приложения (роутеры отличаются по тегам)
    for router in routers_list:
        app.include_router(router)

    app.include_router(system_routers)
    return server
