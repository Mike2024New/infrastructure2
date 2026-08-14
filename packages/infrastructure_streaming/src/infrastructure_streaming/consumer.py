import asyncio, websockets
from typing import Callable


async def consume_stream(
        url: str,
        data: str,
        callback: Callable[[bytes], None],
        event: asyncio.Event,
        timeout: float = 1.0
) -> None:
    """
    Потребитель стрима. Отправляет запрос и получает ответы частями. (подходит для realtime обработки)
    Паттерн 'данные передаются на сервер' -> 'сервер выдает ответ порциями' например ответ от llm, callback обрабатывает
    полученные чанки (порции)
    :param url: url формата websocket, например ws://{host}:{port}/ws
    :param data: передаваемые на сервер данные
    :param callback: функция обрабатывающая ответ сервера, ответ полученный в байтах (обработка ответа - прерогатива callback)
    :param event: прерыватель стрима (установить set во внешнем коде и стрим остановится досрочно)
    :param timeout: ожидание ответа сервера время в секундах
    :return: None
    """
    async with websockets.connect(url) as ws:
        try:
            await ws.send(data)
            while True:
                if event.is_set():
                    print(f'stream cancelled')
                    break
                response = await asyncio.wait_for(ws.recv(), timeout=timeout)
                try:
                    callback(response)
                except Exception as err:
                    raise RuntimeError(f'Callback error: {err}')
        except asyncio.TimeoutError:
            raise
        except websockets.exceptions.ConnectionClosedError:
            pass  # соединение разорвано, обрабатывать через callback
        except Exception as err:
            print(f"stream error: {err}")
            raise
