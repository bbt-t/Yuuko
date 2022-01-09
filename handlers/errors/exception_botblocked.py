from aiogram.utils.exceptions import BotBlocked
from aiogram.types import Update

from loader import dp, logger_guru


@dp.errors_handler(exception=BotBlocked)
async def bot_blocked_error(update: Update, exception: BotBlocked):
    """
    If the user has blocked the bot
    """
    logger_guru.exception(f'Bot blocked by user {update.message.from_user.id}')
    return True
