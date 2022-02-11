from aiogram.dispatcher.filters import Command, Filter
from aiogram.types import Message

from loader import dp
from utils.database_manage.sql.sql_commands import check_valid_user, select_bot_language
from sqlalchemy.exc import NoResultFound


commands: set = {'todo', 'start_weather', 'horoscope', 'hair', 'pass', 'set_time_todo', 'change_skin'}


class IsValid(Filter):
    key = "is_valid"

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

    text_msg: str = 'Выбери скин, иначе никак...' if lang == 'ru' else 'Choose a skin, otherwise nothing...'

    await message.answer(text_msg)
