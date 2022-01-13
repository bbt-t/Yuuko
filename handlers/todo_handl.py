from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram_calendar import simple_cal_callback, SimpleCalendar

from config import time_now
from utils.stickers_info import SendStickers
from loader import dp, bot, logger_guru
from middlewares.throttling import rate_limit
from utils.todo import ToDo, load_todo_obj, dump_todo_obj




@rate_limit(5)
@dp.message_handler(Command('todo'))
async def bot_todo(message: Message, state: FSMContext):
    await message.answer_sticker(SendStickers.yipee_2_girls.value)
    await message.answer('<code>Привет! :)\nдавай запишем что сделать и когда</code>',
                         reply_markup=await SimpleCalendar().start_calendar())
    await state.set_state('todo')
    await message.delete()


@dp.callback_query_handler(simple_cal_callback.filter(), state='todo')
async def process_simple_calendar(call: CallbackQuery, callback_data, state: FSMContext):
    selected, date = await SimpleCalendar().process_selection(call, callback_data)

    if date and selected:
        time_todo = date.date()
        if time_todo < time_now.date():
            await bot.answer_callback_query(call.id, 'Выбрать можно только на сегодня и позже !', show_alert=True)
            await call.message.answer('Выбирай с умом :)', reply_markup=await SimpleCalendar().start_calendar())
        else:
            async with state.proxy() as data:
                data['date']: str = str(time_todo)

            await call.message.edit_text(f'Что планируешь на <code>{time_todo}</code> число?')
            await state.set_state('reception_todo')


@dp.message_handler(state='reception_todo')
async def set_calendar_date(message: Message, state: FSMContext):
    async with state.proxy() as data:
        date: str = data['date']

    name: str = f'pref_todo_{message.from_user.id}'

    if len(message.text) <= 500:
        message_task: list = message.text.split('\n')
        try:
            todo_obj: dict = await load_todo_obj()
            todo_obj[name].__add__(dispositions=message_task, time_todo=date)
        except Exception as err:
            logger_guru.info(f'{repr(err)} : Obj todo not found, create new entry. . .')
            todo_obj: dict = {}
            pref_obj = ToDo(message.from_user.id)
            pref_obj.__add__(dispositions=message_task, time_todo=date)
            todo_obj[name] = pref_obj
        finally:
            await state.finish()
        result: str = '\n'.join(
            f"<code>{i})</code> <b>{val}</b>" for
            i, val in enumerate(todo_obj[name].todo[date], 1)
        )
        await dump_todo_obj(todo_obj)
        await message.answer_sticker(SendStickers.great.value)
        await message.delete()
        await message.answer(f'сделано!\n\nвот список на этот день:\n\n{result}')
    else:
        logger_guru.warning(f'{name} Trying to write a message that is too large.')
        await message.answer_sticker(SendStickers.you_were_bad.value)
        await message.answer('Слишком большое сообщение ! Попробуй написать короче')


@dp.message_handler(state='todo')
async def cancel_todo(message: Message, state: FSMContext):
    await message.answer('Тебе нужно выбрать дату :) попробуй ещё раз')
    await state.finish()
