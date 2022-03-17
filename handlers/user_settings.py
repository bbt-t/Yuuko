from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message

from handlers.states_in_handlers import UserSettingStates
from loader import dp
from middlewares.throttling import rate_limit
from utils.database_manage.sql.sql_commands import DB_USERS
from utils.keyboards.base_settings_kb import settings_keyboard


@rate_limit(2, key='set_settings')
@dp.message_handler(Command('set_settings'))
async def set_user_settings(message: Message, state: FSMContext) -> None:
    if (lang := await DB_USERS.select_bot_language(telegram_id=message.from_user.id)) == 'ru':
        await message.answer(
            'Привет! чего настраиваем?',
            reply_markup=settings_keyboard())
    else:
        await message.answer(
            'Hey! what do we set up?',
            reply_markup=settings_keyboard(lang='en'))
    await message.delete()

    await UserSettingStates.first()
    async with state.proxy() as data:
        data['lang'] = lang
