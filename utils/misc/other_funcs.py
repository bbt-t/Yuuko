from asyncio import get_running_loop
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from datetime import datetime
from typing import Any, Iterator, Literal
from zoneinfo import ZoneInfo

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiohttp import ClientSession

from loader import dp, logger_guru
from utils.database_manage.sql.sql_commands import DB_USERS


def get_time_now(tz: str):
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
    for telegram_id in await DB_USERS.select_all_users():
        await dp.bot.unpin_all_chat_messages(chat_id=telegram_id)
    else:
        logger_guru.warning('Delete all message (pin).')


async def get_image_text(url: str, headers: dict, data) -> str:
    """
    Request to a remote server for the text recognition function.
    :param url: request url
    :param headers: settings
    :param data: data for OCR
    :return: result
    """
    async with ClientSession() as session:
        async with session.post(url=url, headers=headers, data=data) as resp:
            return '\n'.join(await resp.text())


def create_keyboard_button(text: tuple, callback_data: tuple, row: int = 3) -> InlineKeyboardMarkup:
    """

    :param text:
    :param callback_data:
    :param row:
    :return:
    """
    keyboard = InlineKeyboardMarkup(row_width=row)
    button_info: Iterator = map(
        lambda item: dict(zip(('text', 'callback_data'), item)),
        zip(text, callback_data)
    )
    for info in button_info:
        keyboard.insert(InlineKeyboardButton(**info))
    return keyboard
