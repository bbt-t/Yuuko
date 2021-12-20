from asyncio import sleep as asyncio_sleep
from sqlalchemy.exc import IntegrityError

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import Message, CallbackQuery, ChatActions

from data.stickers_info import SendStickers
from loader import bot, dp, logger_guru
from middlewares.throttling import rate_limit
from utils.db_api.sql_commands import add_user
from utils.keyboards.start_settings_kb import start_choice_kb
from utils.notify_users import send_synthesize_voice_by_ya, auth




@rate_limit(5, key='start')
@dp.message_handler(CommandStart())
@auth
async def start_working_with_bot(message: Message):
    """
    Such a response will be sent at the start of communication (/start)
    """
    name: str = message.from_user.full_name
    text: str = f"Привет, {name}!\n\nЯ твой 'домашний' бот,\nчтобы я могла выполнять свои функции " \
           f"ответь пожалуйста на пару вопросов..."
    user_id: int = message.from_user.id
    try:
        await add_user(id=user_id, name=name)
    except IntegrityError:
        logger_guru.warning(f'{user_id=} : Integrity Error in start handler!')
    finally:
        await message.answer_sticker(SendStickers.welcome.value)
        await bot.send_chat_action(user_id, ChatActions.TYPING)
        await asyncio_sleep(2)
        await send_synthesize_voice_by_ya(user_id, text)
        await message.answer(text, reply_markup=start_choice_kb)
    await message.delete()


@dp.callback_query_handler(text='set_todo_inp')
async def inl_test_send(call: CallbackQuery, state: FSMContext):
    await call.message.answer_sticker(SendStickers.seeking.value)
    await call.message.answer('В какое время спрашивать тебя о запланированных делах ?')
    await call.message.edit_reply_markup()
    await state.set_state('set_tntodo')


@dp.callback_query_handler(text='cancel')
async def inl_test_send(call: CallbackQuery, state: FSMContext):
    await call.message.answer_sticker(SendStickers.sad_ok.value)
    await bot.send_chat_action(call.from_user.id, ChatActions.TYPING)
    await asyncio_sleep(1)
    await bot.answer_callback_query(call.id, 'ЖАЛЬ :С если что мои команды можно подглядеть '
                                             'через слеш (/)', show_alert=True)
    await call.message.edit_reply_markup()
    await state.finish()
