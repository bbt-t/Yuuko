import hmac
from pickle import PicklingError, loads, UnpicklingError, dumps
from contextlib import suppress

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram_calendar import simple_cal_callback, SimpleCalendar

from config import pkl_key, time_now
from loader import dp, bot, logger_guru
from middlewares.throttling import rate_limit
from utils.todo import ToDo




def save_pkl_obj():
    """
    Write pickle with signature.
    """
    data = dumps(all_todo_obj)
    digest: bytes = hmac.digest(pkl_key.encode(), data, 'sha256')
    try:
        with open('data/data_todo.pickle', 'wb') as f:
            for items in (digest, b'delimiter', data):
                f.write(items)
    except PicklingError as err:
        logger_guru.error(f'{repr(err)} : Error write pickle !')
    else:
        logger_guru.info('Save pkl object')


def add_all_todo() -> dict:
    """
    Read ToDo objects.
    """
    try:
        with open('data/data_todo.pickle', 'rb') as f:
            digest, new_data = f.read().split(b'delimiter')
            digest_new: bytes = hmac.digest(pkl_key.encode(), new_data, 'sha256')
            if not hmac.compare_digest(digest_new, digest):
                raise UnpicklingError
    except PicklingError as e:
        logger_guru.warning(f'{repr(e)} : Error read pkl object !')
    else:
        logger_guru.info('pkl signatures match !')
        read_obj: dict = loads(new_data)
        return read_obj


try:
    all_todo_obj: dict = add_all_todo()
except FileNotFoundError as err:
    logger_guru.info(f'{repr(err)} : Create new dict object for todo.')
    all_todo_obj: dict = {}


def delete_all_todo():
    date: str = str(time_now.date())

    for item in all_todo_obj.values():
        with suppress(RuntimeError):
            for key in item.todo:
                if key == date:
                    del item.todo[key]


@rate_limit(5)
@dp.message_handler(Command('todo'))
async def bot_todo(message: Message, state: FSMContext):
    await message.reply_sticker('CAACAgIAAxkBAAEDZdthp74uT7HCmBSru9Ehma95SpVSIQACZQEAAhAabSJhjGLAZuk2oSIE')
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

            await call.message.answer(f'Что планируешь на <code>{time_todo}</code> число?')
            await state.set_state('reception_todo')


@dp.message_handler(state='reception_todo')
async def set_calendar_date(message: Message, state: FSMContext):
    async with state.proxy() as data:
        date: str = data['date']
    name: str = f'pref_todo_{message.from_user.id}'
    if len(message.text) <= 120:
        message_task: list = message.text.split(',')
        try:
            all_todo_obj[name].__add__(dispositions=message_task, time_todo=date)
        except Exception as err:
            logger_guru.info(f'{repr(err)} : Obj todo not found, create new entry. . .')

            pref_obj = ToDo(message.from_user.id)
            pref_obj.__add__(dispositions=message_task, time_todo=date)
            all_todo_obj[name] = pref_obj
        finally:
            await state.finish()
        result: str = '\n'.join(
            f"<code>{i})</code> <b>{val}</b>" for
            i, val in enumerate(all_todo_obj[name].todo[date], 1)
        )
        await message.answer(f'сделано!\n\nвот список на этот день:\n\n{result}')
    else:
        logger_guru.warning(f'{name} Trying to write a message that is too large.')
        await message.reply_sticker('CAACAgIAAxkBAAEDZZhhp4W7R60LkP0BQaSR3B-agVBpswACpAEAAhAabSIYtWa5P_cfjSIE')
        await message.answer('Слишком большое сообщение ! Попробуй написать короче')


@dp.message_handler(state='todo')
async def cancel_todo(message: Message, state: FSMContext):
    await message.answer('Тебе нужно выбрать дату :) попробуй ещё раз')
    await state.finish()