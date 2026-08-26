import itertools
import asyncio


async def spiner(text, event: asyncio.Event):
    """Спиннер для ожидания операций время которых заранее не известно"""
    spinner = itertools.cycle(['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'])
    while not event.is_set():
        print(f'\r{next(spinner)} {text}', end='')
        await asyncio.sleep(0.2)
    print(f'\r✔ {text}{" " * 10}')  # перевести каретку


async def main():
    event = asyncio.Event()
    spiner_task = asyncio.create_task(spiner(text='загрузка сервиса `svc_start`', event=event))
    await asyncio.sleep(5)
    event.set()
    await spiner_task


if __name__ == '__main__':
    asyncio.run(main())
