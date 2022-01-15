from collections import defaultdict
from datetime import timedelta

from ujson import loads as ujson_loads
from ujson import dumps as ujson_dumps
from aiofiles import open as aiofiles_open

from config import time_now
from loader import logger_guru




async def dump_todo_obj(todo_obj: dict) -> None:
    """
    Save todo_obj to json-file.
    :param todo_obj: all_todo
    """
    data = ujson_dumps(todo_obj)
    async with aiofiles_open('data/data_todo.json', mode='w') as f:
        await f.write(data)


async def load_todo_obj() -> dict:
    """
    Read ToDo_object.
    """
    try:
        async with aiofiles_open('data/data_todo.json', mode='r') as f:
            read_obj: dict = ujson_loads(await f.read())
    except FileNotFoundError as err:
        logger_guru.warning(f'{repr(err)} : Obj todo not found, create new entry. . .')
        read_obj = defaultdict(dict)

    return read_obj


async def delete_all_todo() -> None:
    """
    Deletes keys at a given time.
    """
    date, read_data = str((time_now - timedelta(days=1)).date()), await load_todo_obj()

    todo_obj: dict = {
        userid: {
            date_key: todo_val for date_key, todo_val in values.items() if date_key != date
        } for userid, values in read_data.items()
    }
    logger_guru.warning('TODO deleted successfully')
    await dump_todo_obj(todo_obj)

