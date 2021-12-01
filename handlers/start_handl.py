from sqlite3 import Error

from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery

from loader import bot, dp, db, logger_guru
from utils.keyboards.start_settings_kb import start_choice_kb




@dp.message_handler(CommandStart())
async def bot_start(message: Message):
    """
    Such a response will be sent at the start of communication (/start)
    """
    name: str = message.from_user.full_name
    try:
        db.add_user(message.from_user.id, name)
    except Error as err:
        logger_guru.warning(repr(err))
    finally:
        await message.answer(f"Привет, {name}!\n\n"
                             f"Я твой 'домашний' бот :)\nчтобы я мог тебе помогать ответь на пару вопросов\n"
                             f"Согласен?", reply_markup=start_choice_kb)


@dp.callback_query_handler(text='set_todo_inp')
async def inl_test_send(call: CallbackQuery, state: FSMContext):
    await call.message.answer('В какое время спрашивать тебя о запланированных делах в конце дня?\n\n'
                              'напиши время в формате  ->  <CODE>ЧАС : МИНУТЫ</CODE>\n\n')
    await call.message.edit_reply_markup()
    await state.set_state('set_tntodo')


@dp.callback_query_handler(text='cancel')
async def inl_test_send(call: CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(call.id, 'ЖАЛЬ :С\n\nесли передумаешь загляни в '
                                             'спискок команд ...', show_alert=True)
    await call.message.edit_reply_markup()
    await state.finish()