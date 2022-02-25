from aiogram.types import Update
from aiogram.utils.exceptions import MessageNotModified

from loader import dp, logger_guru


@dp.errors_handler(exception=MessageNotModified)
async def error_bot_blocked(update: Update, exception: MessageNotModified) -> bool:
    logger_guru.warning(f"Can'not modified message!\n{update=}\n{exception=}")
    return True
