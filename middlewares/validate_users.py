from aiogram.types import Message
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware

from utils.database_manage.sql.sql_commands import check_invalid_user


class ValidateUsers(BaseMiddleware):

    async def on_pre_process_message(self, message: Message, data: dict):
        commands: set = {'/todo', '/horoscope', '/hair', '/pass', '/support', '/set_settings'}
        if message.text in commands and await check_invalid_user(telegram_id=message.from_user.id):
            await message.answer('start the bot again 💬 /start')
            raise CancelHandler()
