from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup

from handlers.states_in_handlers import UserSettingStates
from loader import dp
from middlewares.throttling import rate_limit
from utils.database_manage.sql.sql_commands import DB_USERS
from utils.keyboards.base_settings_kb import settings_keyboard, choice_settings


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


@dp.callback_query_handler(text={'set_time_todo', 'set_weather'}, state=UserSettingStates.settings)
async def weather_notification_settings(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        lang: str = data.get('lang')

    match call.data:
        case 'set_time_todo':
            keyboard: InlineKeyboardMarkup = choice_settings(is_todo=True, lang=lang)
        case 'set_weather':
            keyboard: InlineKeyboardMarkup = choice_settings(is_weather=True, lang=lang)

    await call.message.edit_text(
        'Что делаем?' if lang == 'ru' else 'What do we do?',
        reply_markup=keyboard
    )
