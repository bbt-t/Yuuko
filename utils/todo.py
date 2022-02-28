from collections import defaultdict
from datetime import timedelta

from ujson import loads as ujson_loads
from ujson import dumps as ujson_dumps
from aiofiles import open as aiofiles_open

from config import time_zone
from loader import dp, logger_guru
from utils.misc.other_funcs import get_time_now


async def dump_todo_obj(todo_obj: dict) -> None:
    """
    Save todo_obj to json-file.
    :param todo_obj: all_todo
    """
    data = ujson_dumps(todo_obj)
    async with aiofiles_open('data/db/data_todo.json', mode='w') as f:
        await f.write(data)


async def load_todo_obj() -> dict:
    """
    Read ToDo_object.
    """
    try:
        async with aiofiles_open('data/db/data_todo.json', mode='r') as f:
            read_obj: dict = ujson_loads(await f.read())
    except FileNotFoundError as err:
        logger_guru.warning(f'{repr(err)} : Obj todo not found, create new entry. . .')
        read_obj = defaultdict(dict)

    return read_obj


async def delete_all_todo() -> None:
    """
    Deletes keys at a given time.
    """
    todo_obj = defaultdict(dict)
    date, read_data = (get_time_now(time_zone) - timedelta(days=1)).strftime('%Y-%m-%d'), await load_todo_obj()

    clear_todo_obj: dict = {
        userid: {
            date_key: todo_val for date_key, todo_val in values.items() if date_key != date
        } for userid, values in read_data.items()
    }

    todo_obj |= clear_todo_obj
    await dump_todo_obj(todo_obj)

    logger_guru.warning('TODO deleted successfully')


async def pin_todo_message(chat_id: int | str, msg_id: int | str, disable_notification: bool = True) -> None:
    """
    Pins a message.
    :param msg_id: id of the message to pin
    :param chat_id: id of the chat from which the message should be pined
    :param disable_notification: disable alert
    """
    await dp.bot.unpin_all_chat_messages(chat_id=chat_id)
    await dp.bot.pin_chat_message(chat_id=chat_id, message_id=msg_id, disable_notification=disable_notification)

    logger_guru.info(f'{msg_id=} message pin')
