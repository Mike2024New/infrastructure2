import asyncio
from infrastructure_streaming.stream_v1.examples.server import Server
from infrastructure_streaming.stream_v1 import stream_pipeline, StreamPipe


async def main():
    port1 = 8001
    port2 = 8002
    server1 = Server(port=port1)
    server2 = Server(port=port2)
    asyncio.create_task(server1.start())
    asyncio.create_task(server2.start())
    queue = asyncio.Queue()

    async def callback_step1(data, _: asyncio.Event):
        await queue.put(data)

    async def callback_step2(_: asyncio.Event):
        data = await queue.get()
        return data

    async def callback_step3(data, _: asyncio.Event):
        print(data)

    # клиент потребляет чанки, например audio_input
    step1 = StreamPipe(
        type='consumer',
        url=f'ws://localhost:{port1}/ws_producer',
        callback=callback_step1,
    )

    # клиент передает чанки, например в vad
    step2 = StreamPipe(
        type='producer',
        url=f'ws://localhost:{port2}/ws_echo',
        callback=callback_step2,
    )

    # клиент получает чанки из vad
    step3 = StreamPipe(
        type='consumer',
        url=f'ws://localhost:{port2}/ws_echo',
        callback=callback_step3,
    )

    event = asyncio.Event()
    stream_task = asyncio.create_task(
        stream_pipeline(
            event=event,
            callback_list=[
                step1,  # получает данные от 1 сервера
                step2,  # пересылает данные на 2 сервер для их обработки
                step3,  # получает обработанные данные с 2 сервера
            ],
        )
    )

    await asyncio.to_thread(lambda: input('press enter for exit\n'))
    event.set()
    await stream_task
    await  server1.stop()
    await  server2.stop()


if __name__ == '__main__':
    asyncio.run(main())
