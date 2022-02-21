from aiogram.dispatcher.filters import Command, Filter
from aiogram.types import Message

from loader import dp
from utils.database_manage.sql.sql_commands import check_valid_user, select_bot_language
from sqlalchemy.exc import NoResultFound


commands: frozenset = frozenset({'todo', 'horoscope', 'hair', 'pass', 'set_settings'})


class IsValid(Filter):
    key: str = "is_valid"

    async def check(self, message: Message):
        return await check_valid_user(telegram_id=message.from_user.id)


@dp.message_handler(Command(commands), IsValid())
async def check_for_validity(message: Message):
    """
    Сhecks if the user has selected a skin.
    :param message: commands from the list (commands)
    """
    try:
        lang: str = await select_bot_language(telegram_id=message.from_user.id)
    except NoResultFound:
        return await message.answer('start the bot again or /start')
    await message.answer(
        'Выбери скин, иначе никак...' if lang == 'ru' else 'Choose a skin, otherwise nothing...'
    )
