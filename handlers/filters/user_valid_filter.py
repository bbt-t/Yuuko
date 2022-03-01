from aiogram.dispatcher.filters import Command, Filter
from aiogram.types import Message

from loader import dp
from utils.database_manage.sql.sql_commands import check_valid_user


commands: set = {'todo', 'horoscope', 'hair', 'pass', 'support', 'set_settings'}


class IsValid(Filter):
    """
    Filters out users without an entry in the DB.
    """
    key: str = "is_valid"

    async def check(self, message: Message) -> bool:
        return await check_valid_user(telegram_id=message.from_user.id)


@dp.message_handler(Command(commands), IsValid())
async def check_for_validity(message: Message) -> None:
    """
    Сheck user.
    :param message: commands from the list (commands)
    """
    await message.answer('start the bot again or /start')
