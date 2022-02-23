from asyncio import get_running_loop
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo

from aiohttp import ClientSession

from loader import dp, logger_guru
from utils.database_manage.sql.sql_commands import select_all_user


def get_time_now(tz: str):
    """
    Take time and date in the time-zone.
    :param tz: time-zone
    :return: datatime object
    """
    zone = ZoneInfo(tz)
    return datetime.now(tz=zone)


async def blocking_io_run_func(func, *args) -> Any:
    """
    Run in a custom thread pool (IO).
    :param func: func to run in the pool
    :param args: func arguments
    :return: func result
    """
    loop = get_running_loop()
    with ThreadPoolExecutor() as pool:
        result = await loop.run_in_executor(pool, func, *args)
    return result


async def cpu_bound_run_func(func, *args) -> Any:
    """
    Run in a custom process pool (CPU-bound operations).
    :param func: func to run in the pool
    :param args: func arguments
    :return: func result
    """
    loop = get_running_loop()
    with ProcessPoolExecutor() as pool:
        result = await loop.run_in_executor(pool, func, *args)
    return result


async def delete_marked_message(msg_id: int | str, chat_id: int) -> None:
    """
    Deletes the message.
    :param msg_id: id of the message to be deleted
    :param chat_id: id of the chat from which the message should be deleted
    """
    await dp.bot.delete_message(chat_id=chat_id, message_id=msg_id)


async def pin_todo_list(msg_id: int | str, chat_id: int) -> None:
    """
    Pins a message.
    :param msg_id: id of the message to pin
    :param chat_id: id of the chat from which the message should be pined
    """
    await dp.bot.unpin_all_chat_messages(chat_id=chat_id)
    await dp.bot.pin_chat_message(chat_id=chat_id, message_id=msg_id, disable_notification=True)

    logger_guru.info(f'{msg_id=} message pin')


async def clear_all_pin_msg() -> None:
    """
    Unpin all messages.
    """
    for telegram_id in await select_all_user():
        await dp.bot.unpin_all_chat_messages(chat_id=telegram_id)
    else:
        logger_guru.warning('Delete all message (pin).')


async def get_image_text(url: str, headers: dict, data) -> str:
    async with ClientSession() as session:
        async with session.post(url=url, headers=headers, data=data) as resp:
            return '\n'.join(await resp.text())