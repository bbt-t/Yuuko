from aiogram.types import Update
from aiogram.utils.exceptions import MessageCantBeEdited

from loader import dp, logger_guru


@dp.errors_handler(exception=MessageCantBeEdited)
async def error_msg_edit(update: Update, exception: MessageCantBeEdited) -> bool:
    """
    If the message cannot be changed.
    :param exception: exception name
    """
    logger_guru.warning(f"Message can't be edited!\n{update=}\n{exception=}")
    return True
