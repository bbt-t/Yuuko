from asyncio import sleep as asyncio_sleep
from sqlalchemy.exc import IntegrityError

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import Message, CallbackQuery, ChatActions
from aiogram_calendar import simple_cal_callback, SimpleCalendar

from config import time_zone
from utils.enums_data import SendStickers
from loader import dp, logger_guru, get_time_now
from middlewares.throttling import rate_limit
from utils.db_api.sql_commands import add_user, update_birthday
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
    text: str = (
        f"Привет, {name}!\n\nЯ твой 'домашний' бот,\n"
        f"чтобы я могла выполнять свои функции ответь пожалуйста на пару вопросов..."
    )
    user_id: int = message.from_user.id
    try:
        await add_user(id=user_id, name=name)
    except IntegrityError:
        logger_guru.warning(f'{user_id=} : Integrity Error in start handler!')
    finally:
        await message.answer_sticker(SendStickers.welcome.value)
        await dp.bot.send_chat_action(user_id, ChatActions.TYPING)
        await asyncio_sleep(2)
        await send_synthesize_voice_by_ya(user_id, text)
        await message.answer(text, reply_markup=start_choice_kb)


@dp.callback_query_handler(text='set_birthday')
async def indicate_date_of_birth(call: CallbackQuery, state: FSMContext):
    await call.message.answer_sticker(SendStickers.seeking.value)
    await call.message.edit_text('Укажи свой ДР (настоящее, его всёравно никто не увидит кроме меня:))')
    await call.message.edit_reply_markup(await SimpleCalendar().start_calendar())
    await state.set_state('set_birthday_and_todo')


@dp.callback_query_handler(simple_cal_callback.filter(), state='set_birthday_and_todo')
async def birthday_simple_calendar(call: CallbackQuery, callback_data, state: FSMContext):
    selected, date = await SimpleCalendar().process_selection(call, callback_data)
    if date and selected:
        time_todo = date.date()
        if time_todo > get_time_now(time_zone).date():
            await dp.bot.answer_callback_query(call.id, 'Выбрать можно только на сегодня и позже !', show_alert=True)
            await call.message.answer(
                'Ты не можешь выбрать эту дату!',
                reply_markup=await SimpleCalendar().start_calendar())
        else:
            await update_birthday(id=call.from_user.id, birthday=date.date())
            await call.message.answer('В какое время спрашивать тебя о запланированных делах ?')
            await state.set_state('set_tntodo')


@dp.callback_query_handler(text='cancel', state='*')
async def exit_handling(call: CallbackQuery, state: FSMContext):
    await call.message.answer_sticker(SendStickers.sad_ok.value)
    await dp.bot.send_chat_action(call.from_user.id, ChatActions.TYPING)
    await asyncio_sleep(1)
    await dp.bot.answer_callback_query(call.id, 'ЖАЛЬ :С если что мои команды можно подглядеть '
                                             'через слеш (/)', show_alert=True)
    await call.message.delete_reply_markup()
    await state.finish()
