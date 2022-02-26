from asyncio import get_running_loop
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from datetime import datetime
from time import sleep
from typing import Any
from zoneinfo import ZoneInfo

from aiohttp import ClientSession
from aiogram.utils.exceptions import BotBlocked

from loader import dp, logger_guru
from utils.database_manage.sql.sql_commands import select_all_users


def get_time_now(tz: str) -> datetime:
    """
    Take time and date in the time-zone.
    :param tz: time-zone
    :return: datatime object
    """
    result = datetime.now(tz=ZoneInfo(tz))
    return result


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


async def clear_all_pin_msg() -> None:
    """
    Unpin all messages.
    """
    for telegram_id in await select_all_users():
        await dp.bot.unpin_all_chat_messages(chat_id=telegram_id)
    else:
        logger_guru.warning('Delete all message (pin).')


async def get_image_text(url: str, headers: dict, data) -> str:
    async with ClientSession() as session:
        async with session.post(url=url, headers=headers, data=data) as resp:
            return '\n'.join(await resp.text())


async def send_a_message_to_all_users(msg: str) -> None | str:
    """
    When sending notifications to multiple users,
    the API will not allow sending more than 30 messages per second.
    :param msg: text to send
    :return: None if everything went well, else user id that caused the error
    """
    counter = 0
    for telegram_id in await select_all_users():
        try:
            if counter < 10:
                await dp.bot.send_message(chat_id=telegram_id, text=msg)
                counter += 1
            else:
                sleep(1)
                counter = 0
        except BotBlocked:
            logger_guru.warning(f'{telegram_id} : error when trying to send')
            return f'mistakes: {telegram_id}'
