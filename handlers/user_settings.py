from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message

from loader import dp
from middlewares.throttling import rate_limit
from utils.database_manage.sql.sql_commands import select_bot_language
from utils.keyboards.base_settings_kb import settings_keyboard_ru, settings_keyboard_en


@rate_limit(5, key='set_settings')
@dp.message_handler(Command('set_settings'))
async def set_user_settings(message: Message, state: FSMContext):
    if (lang := await select_bot_language(telegram_id=message.from_user.id)) == 'ru':
        await message.answer('Привет! чего настраиваем?', reply_markup=settings_keyboard_ru)
    else:
        await message.answer('Hey! what do we set up?', reply_markup=settings_keyboard_en)

    await state.set_state('settings')
    async with state.proxy() as data:
        data['lang'] = lang

    await message.delete()
