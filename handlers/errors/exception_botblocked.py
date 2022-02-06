from aiogram.types import Update
from aiogram.utils.exceptions import BotBlocked

from loader import dp, logger_guru


@dp.errors_handler(exception=BotBlocked)
async def bot_blocked_error(update: Update, exception: BotBlocked):
    """
    If the user has blocked bot.
    """
    logger_guru.exception(f'Bot blocked by user {update.message.from_user.id}')
    return True
