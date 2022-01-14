from datetime import timedelta

from ujson import loads as ujson_loads
from ujson import dumps as ujson_dumps
from aiofiles import open as aiofiles_open

from config import time_now




async def dump_todo_obj(todo_obj: dict) -> None:
    """
    Save todo_obj to pickle-file.
    :param todo_obj: all_todo
    """
    data = ujson_dumps(todo_obj)
    async with aiofiles_open('data/data_todo.json', mode='w') as f:
        await f.write(data)


async def load_todo_obj() -> dict:
    """
    Read ToDo_object.
    """
    async with aiofiles_open('data/data_todo.json', mode='r') as f:
        read_obj: dict = ujson_loads(await f.read())
    return read_obj


async def delete_all_todo() -> None:
    """
    Deletes keys at a given time.
    """
    date = str((time_now - timedelta(days=1)).date())

    todo_obj: dict = {
        user_id: {
            date_key: todo_val for date_key, todo_val in values.items() if date_key != date
        } for user_id, values in (await load_todo_obj()).items()
    }

    await dump_todo_obj(todo_obj)
