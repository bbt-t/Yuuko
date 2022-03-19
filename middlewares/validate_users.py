from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import Message
from aioredis.exceptions import ConnectionError
from sqlalchemy.exc import NoResultFound

from config import bot_administrators
from loader import dp, logger_guru
from utils.database_manage.sql.sql_commands import DB_USERS
from utils.misc.notify_admins import on_shutdown_notify


class CustomValidate(BaseMiddleware):
    """
    User and msg verification:
        Presence of a user in the database
        Command write prevention
    Stop bot if connection to radis fails.
    """
    commands: set = {'/start', '/todo', '/horoscope', '/hair', '/pass', '/support', '/set_settings', '/recipe'}

    async def on_pre_process_message(self, message: Message, data: dict) -> None:
        """
        Denying access to the bot to users who do not have an entry in the database.
        Prohibition of the use of commands in the "to-do-handler"... etc.
        """
        try:
            if message.get_command() in self.commands:
                if message.get_command() != '/start' and await DB_USERS.check_invalid_user(message.from_user.id):
                    await message.answer('start the bot again 💬 /start')
                    raise CancelHandler()
                elif await (state := dp.current_state(chat=message.chat.id, user=message.from_user.id)).get_state():
                    await message.reply('ХММ...', allow_sending_without_reply=False)
                    await state.finish()
                    raise CancelHandler()
        except ConnectionError as err:
            text_msg_ru: str = 'Что-то пошло не так, мы уже решаем эту проблему, попробуй позже...'
            text_msg_en: str = 'Something went wrong, we are already solving this problem, please try again later...'
            try:
                lang, skin = await DB_USERS.select_lang_and_skin(telegram_id=message.from_user.id)
            except NoResultFound:
                await message.answer(text_msg_en)
            else:
                await message.answer_sticker(skin.something_is_wrong.value)
                await message.answer(text_msg_ru if lang == 'ru' else text_msg_en)
            finally:
                await dp.bot.send_message(
                    chat_id=bot_administrators.get('creator'),
                    text='⚠ <b>Error connecting 🔌 redis!</b> ⚠\n'
                         '⚠ <b>Restart Redis or run bot in <code>--mem</code> mode !</b> ⚠'
                )
                await on_shutdown_notify(dp)
                raise SystemExit(f'{repr(err)} : Error connecting to redis!')
