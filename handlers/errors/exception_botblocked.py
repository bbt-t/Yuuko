from aiogram.types import Update
from aiogram.utils.exceptions import BotBlocked

from config import bot_administrators
from loader import dp, logger_guru
from utils.database_manage.sql.sql_commands import DB_USERS


@dp.errors_handler(exception=BotBlocked)
async def bot_blocked_error(update: Update, exception: BotBlocked) -> bool:
    """
    If the user has blocked bot.
    :param exception: exception name
    """
    user_id: int = update.message.from_user.id
    logger_guru.exception(f'Bot blocked by {user_id=}')
    try:
        await DB_USERS.delete_user(user_id)
    except BaseException as err:
        logger_guru.warning(f"{repr(err)} : Can't delete {user_id=}")
        await dp.bot.send_message(
            chat_id=bot_administrators.get('creator'),
            text=f"{user_id=} : Can't delete user!\n{update}\n{exception}"
        )
    return True
