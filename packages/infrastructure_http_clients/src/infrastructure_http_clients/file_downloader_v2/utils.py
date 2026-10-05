import asyncio


async def observer(feedback_dict_in: dict, event_in: asyncio.Event):
    while not event_in.is_set():
        await asyncio.sleep(0.1)
        row = " | ".join([f"{k} : {v}%" for k, v in feedback_dict_in.items()])
        print(f'\r{row}', end='')
