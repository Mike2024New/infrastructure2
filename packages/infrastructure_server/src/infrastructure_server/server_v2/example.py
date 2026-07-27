from fastapi import APIRouter
from infrastructure_server import server_factory_v2

# Подключение роутеров, с бизнес логикой приложения
demo_router = APIRouter(tags=['demo'], prefix='/demo')


@demo_router.get('/')
def demo():
    return {'msg': 'demo'}


# создание сервера
server1 = server_factory_v2(
    app_name='main',
    routers_list=[demo_router],  # добавление дополнительных эндпоинтов
    callback_start=lambda details: print(f'server start, details: {details}'),
    callback_start_error=lambda details: print(f'server runned error: {details}'),
    callback_end=lambda details: print(f'server stop, details: {details}'),
    api_pid=True,  # получение PID сервера (не использовать для публичных api)
    api_shudtown=True,  # возможность отключить сервер через http (не использовать для публичных api)
)
server1.start(host='localhost', port=8000, log_level='info')  # запуск сервера. Остановка через http
