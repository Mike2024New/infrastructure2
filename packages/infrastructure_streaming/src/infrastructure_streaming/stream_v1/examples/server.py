import asyncio, uvicorn
from fastapi import FastAPI, WebSocket
from starlette.websockets import WebSocketDisconnect


class Server:
    def __init__(self, host='localhost', port=8000):
        self._app = FastAPI()
        self._host = host
        self._port = port
        self._server = None

        @self._app.websocket('/ws_producer')
        async def stream_producer(websocket: WebSocket):
            await websocket.accept()
            try:
                i = 0
                while self._server is not None:
                    await websocket.send_json({'data': f'chunk_{i}'})
                    await asyncio.sleep(0.2)
                    i += 1
            except WebSocketDisconnect:
                print(f'Клиент отключился')

        @self._app.websocket('/ws_echo')
        async def stream_echo(websocket: WebSocket):
            await websocket.accept()
            try:
                while self._server is not None:
                    try:
                        # принимает результат обрабатывает
                        result = await asyncio.wait_for(websocket.receive_json(), timeout=1)
                        await websocket.send_json(result)
                    except asyncio.TimeoutError:
                        pass
            except WebSocketDisconnect:
                print(f'Клиент отключился')

    async def start(self):
        """Запуск сервера"""
        config = uvicorn.Config(
            app=self._app,
            host=self._host,
            port=self._port,
            log_level="warning",
        )
        self._server = uvicorn.Server(config)
        await self._server.serve()

    async def stop(self):
        """Остановка сервера"""
        if self._server:
            self._server.should_exit = True
            await self._server.shutdown()
            self._server = None


async def main():
    port = 8000
    server = Server(port=port)
    asyncio.create_task(server.start())
    await asyncio.to_thread(lambda: input('\npress enter for exit\n'))
    await  server.stop()


if __name__ == '__main__':
    asyncio.run(main())
