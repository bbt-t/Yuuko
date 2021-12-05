from asyncio import sleep as asyncio_sleep
from sqlite3 import Error

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import Message, CallbackQuery, ChatActions

from loader import bot, dp, db, logger_guru
from middlewares.throttling import rate_limit
from utils.keyboards.start_settings_kb import start_choice_kb
from utils.notify_users import send_synthesize_voice_by_ya, auth




@dp.message_handler(CommandStart())
@rate_limit(5)
@auth
async def bot_start(message: Message):
    """
    Such a response will be sent at the start of communication (/start)
    """
    name: str = message.from_user.full_name
    text = f"Привет, {name}!\n\nЯ твой 'домашний' бот,\nчтобы я могла выполнять свои функции " \
           f"ответь пожалуйста на пару вопросов..."
    try:
        db.add_user(message.from_user.id, name)
    except Error as err:
        logger_guru.warning(repr(err))
    finally:
        await message.answer_sticker('CAACAgIAAxkBAAEDZZZhp4UKWID3NNoRRLywpZPBSmpGUwACVwEAAhAabSKlKzxU-3o0qiIE')
        await bot.send_chat_action(message.chat.id, ChatActions.TYPING)
        await asyncio_sleep(2)
        await send_synthesize_voice_by_ya(message.from_user.id, text)
        await message.answer(text, reply_markup=start_choice_kb)


@dp.callback_query_handler(text='set_todo_inp')
async def inl_test_send(call: CallbackQuery, state: FSMContext):
    await call.message.answer_sticker('CAACAgIAAxkBAAEDZZphp4c3RNVqorg6zd0JRBzjB29bXwACcAEAAhAabSIN3A9bRLCgiyIE')
    await call.message.answer('В какое время спрашивать тебя о запланированных делах ?')
    await call.message.edit_reply_markup()
    await state.set_state('set_tntodo')


@dp.callback_query_handler(text='cancel')
async def inl_test_send(call: CallbackQuery, state: FSMContext):
    await call.message.answer_sticker('CAACAgIAAxkBAAEDZaNhp4w03jKO6vfOzbiZ7E13RAwaZwACYQEAAhAabSLviIx9qppNByIE')
    await bot.send_chat_action(call.from_user.id, ChatActions.TYPING)
    await asyncio_sleep(1)
    await bot.answer_callback_query(call.id, 'ЖАЛЬ :С если что мои команды можно подглядеть '
                                             'через слеш (/)', show_alert=True)
    await call.message.edit_reply_markup()
    await state.finish()

