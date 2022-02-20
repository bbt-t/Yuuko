from aiogram.types import Update
from aiogram.utils.exceptions import MessageCantBeDeleted

from loader import dp, logger_guru


@dp.errors_handler(exception=MessageCantBeDeleted)
async def error_msg_edit(update: Update, exception: MessageCantBeDeleted):
    """
    If the message cannot be deleted.
    :param exception: exception name
    """
    logger_guru.warning(f"Message can't be edited!\nСообщение: {update}\nОшибка: {exception}")
    return True
