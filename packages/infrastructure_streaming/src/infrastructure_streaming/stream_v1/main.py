import asyncio
from websockets.exceptions import ConnectionClosedError, ConnectionClosedOK
import websockets
from dataclasses import dataclass
from typing import Literal, Awaitable, Callable, Any

__all__ = ['StreamPipe', 'stream_pipeline']


@dataclass
class StreamPipe:
    type: Literal['consumer', 'producer']
    url: str
    callback: Callable[[Any, asyncio.Event], Awaitable[None]] | Callable[[asyncio.Event], Awaitable[None]]
    callback_error: Callable[[asyncio.Event, Exception], Awaitable[None]] | None = None


async def connect_websocket(url: str) -> websockets.ClientConnection:
    """Получение соединения"""
    ws = await websockets.connect(url)
    return ws


async def send(ws, callback, event: asyncio.Event):
    """Отправка данных на сервер, применение callback_consumer"""
    res = await callback(event)
    if res is not None:
        await ws.send(res)
    else:
        event.set()


async def get(ws, callback, event: asyncio.Event, timeout: float = 1):
    if callback is None:
        return
    try:
        data = await asyncio.wait_for(ws.recv(), timeout=timeout)
        await callback(data, event)
    except asyncio.TimeoutError:
        pass
    except (ConnectionClosedError, ConnectionClosedOK) as err:
        print(f"Соединение закрыто: {err}")
        event.set()
        return


async def stream_pipeline(
        event: asyncio.Event,
        callback_list: list[StreamPipe],
):
    """
    🚀 Оркестратор WebSocket-стримов.

    Собирает несколько стримов (consumer/producer) в один конвейер,
    управляет подключениями и передачей данных между ними.

    📌 Как это работает:
    Вы передаёте список колбэков, каждый из которых либо:
    - consumer: получает данные от сервера
    - producer: отправляет данные на сервер

    Функция автоматически:
    - подключается к каждому URL
    - переиспользует соединения
    - выполняет колбэки по кругу (round-robin)
    - останавливается по сигналу event

    :param event: флаг остановки
    :param callback_list: список объектов StreamPipe с callback функциями
    :return: None

    (см. подробные примеры в infrastructure_streaming.stream_v1.examples)
    """
    websockets_register = {}
    try:
        while not event.is_set():
            try:
                for callback in callback_list:
                    if event.is_set():
                        break

                    if callback.url not in websockets_register:
                        ws = await connect_websocket(callback.url)
                        websockets_register[callback.url] = ws

                    try:
                        if callback.type == 'consumer':
                            await get(websockets_register[callback.url], callback.callback, event)
                        elif callback.type == 'producer':
                            await send(websockets_register[callback.url], callback.callback, event)
                    except Exception as err:
                        if callback.callback_error is not None:
                            await callback.callback_error(event, err)

                await asyncio.sleep(0.0)

            except (ConnectionClosedError, ConnectionClosedOK):
                break
            except Exception:
                raise
    except Exception as err:
        raise err
