from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import Message

from loader import dp
from utils.database_manage.sql.sql_commands import check_invalid_user


class ValidateMessage(BaseMiddleware):
    """
    User and msg verification:
        Presence of a user in the database
        Command write prevention
    """
    async def on_pre_process_message(self, message: Message, data: dict) -> None:
        """
        Denying access to the bot to users who do not have an entry in the database.
        Prohibition of the use of commands in the "to-do-handeler"... etc.
        """
        commands: set = {'/todo', '/horoscope', '/hair', '/pass', '/support', '/set_settings'}
        if message.get_command() in commands:
            if await check_invalid_user(telegram_id=message.from_user.id):
                await message.answer('start the bot again 💬 /start')
                raise CancelHandler()
            elif await (state := dp.current_state(chat=message.chat.id, user=message.from_user.id)).get_state():
                await message.reply('ХММ...', allow_sending_without_reply=False)
                await state.finish()
                raise CancelHandler()
