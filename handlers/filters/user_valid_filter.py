from aiogram.dispatcher.filters import Command, Filter
from aiogram.types import Message

from loader import dp
from utils.database_manage.sql.sql_commands import check_valid_user, select_bot_language


commands: set = {'todo', 'start_weather', 'horoscope', 'hair', 'pass', 'set_time_todo '}


class IsValid(Filter):
    key = "is_valid"

    async def check(self, message: Message):
        return await check_valid_user(telegram_id=message.from_user.id)


@dp.message_handler(Command(commands), IsValid())
async def id_example(message: Message):
    lang: str = await select_bot_language(telegram_id=message.from_user.id)
    text_msg: str = 'Выбери скин, иначе никак...' if lang == 'ru' else 'Choose a skin, otherwise nothing...'

    await message.answer(text_msg)
