from aiogram.utils.exceptions import MessageNotModified
from aiogram.types import Update

from loader import dp, logger_guru


@dp.errors_handler(exception=MessageNotModified)
async def error_bot_blocked(update: Update, exception: MessageNotModified):
    logger_guru.warning(f"Can'not modified message!\nСообщение: {update}\nОшибка: {exception}")
    return True
