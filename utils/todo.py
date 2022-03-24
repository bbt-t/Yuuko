from collections import defaultdict
from datetime import timedelta
from typing import DefaultDict

from ujson import loads as ujson_loads
from ujson import dumps as ujson_dumps
from aiofiles import open as aiofiles_open

from config import bot_config
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


async def load_todo_obj() -> DefaultDict:
    """
    Read ToDo_object.
    """
    todo_obj: DefaultDict = defaultdict(dict)
    try:
        async with aiofiles_open('data/db/data_todo.json', mode='r') as f:
            read_obj: dict = ujson_loads(await f.read())
            todo_obj |= read_obj
    except FileNotFoundError as err:
        logger_guru.warning(f'{repr(err)} : Obj todo not found, create new entry. . .')
    return todo_obj


async def delete_all_todo() -> None:
    """
    Deletes keys at a given time.
    """
    todo_obj: DefaultDict = defaultdict(dict)

    date: str = (get_time_now(bot_config.time_zone) - timedelta(days=1)).strftime('%Y-%m-%d')
    read_data: DefaultDict = await load_todo_obj()
    clear_todo_obj: dict = {
        userid: {
            date_key: todo_val for date_key, todo_val in values.items() if date_key != date
        } for userid, values in read_data.items()
    }
    logger_guru.warning('TODO deleted successfully')
    todo_obj |= clear_todo_obj
    await dump_todo_obj(clear_todo_obj)


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
