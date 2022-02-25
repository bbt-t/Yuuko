from aiogram.types import Update
from aiogram.utils.exceptions import BotBlocked

from config import bot_administrators
from loader import dp, logger_guru
from utils.database_manage.sql.sql_commands import delete_user


@dp.errors_handler(exception=BotBlocked)
async def bot_blocked_error(update: Update, exception: BotBlocked) -> bool:
    """
    If the user has blocked bot.
    :param exception: exception name
    """
    user_id: int = update.message.from_user.id
    logger_guru.exception(f'Bot blocked by user {user_id=}')
    try:
        await delete_user(user_id)
    except:
        logger_guru.warning(f"{user_id=} : Can't delete user.")
        await dp.bot.send_message(
            chat_id=bot_administrators.get('creator'),
            text=f"{user_id=} : Can't delete user!\n{update}\n{exception}"
        )
    return True
