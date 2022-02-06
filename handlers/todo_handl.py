from datetime import timedelta

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram_calendar import simple_cal_callback, SimpleCalendar

from config import time_zone
from loader import dp, logger_guru, scheduler
from middlewares.throttling import rate_limit
from utils.database_manage.sql.sql_commands import select_skin, select_lang_and_skin
from utils.misc.other_funcs import pin_todo_list, get_time_now
from utils.todo import load_todo_obj, dump_todo_obj


@rate_limit(5)
@dp.message_handler(Command('todo'))
async def bot_todo(message: Message, state: FSMContext):
    lang, skin = await select_lang_and_skin(telegram_id=message.from_user.id)

    await message.answer_sticker(skin.love_you.value)
    await message.answer(
        '<code>Привет! :)\nдавай запишем что сделать и когда</code>',
        reply_markup=await SimpleCalendar().start_calendar())

    await state.set_state('todo')
    async with state.proxy() as data:
        data['lang'] = lang
    await message.delete()


@dp.callback_query_handler(simple_cal_callback.filter(), state='todo')
async def process_simple_calendar(call: CallbackQuery, callback_data, state: FSMContext):
    async with state.proxy() as data:
        lang: str = data.get('lang')
    selected, date = await SimpleCalendar().process_selection(call, callback_data)

    if date and selected:
        time_todo = date.date()
        if time_todo < get_time_now(time_zone).date():
            await dp.bot.answer_callback_query(
                call.id,
                'Выбрать можно только на сегодня и позже !' if lang == 'ru' else
                'You can only choose for today and later!', show_alert=True
            )
            await call.message.answer(
                'Выбирай с умом :)' if lang == 'ru' else 'Choose wisely :)',
                reply_markup=await SimpleCalendar().start_calendar()
            )
        else:
            async with state.proxy() as data:
                data['date']: str = str(time_todo)

            await call.message.edit_text(
                f'Что планируешь на <code>{time_todo}</code> число?' if lang == 'ru' else
                f'What are you planning for the <code>{time_todo}</code>?'
            )
            await state.set_state('reception_todo')


@dp.message_handler(state='reception_todo')
async def set_calendar_date(message: Message, state: FSMContext):
    async with state.proxy() as data:
        lang, date = data.values()
    user_id: int = message.from_user.id
    name, skin = f'todo_{user_id}', await select_skin(telegram_id=user_id)

    if len(message.text) <= 1000:
        message_task: list = message.text.split('\n')
        todo_obj: dict = await load_todo_obj()
        try:
            todo_obj[name][date].extend(message_task)
        except KeyError as err:
            logger_guru.info(f'{repr(err)} : Key not found, create new.')
            todo_obj[name][date] = message_task
        finally:
            await message.delete()
            await state.finish()

        result: str = '\n'.join(f"<code>{i})</code> <b>{val}</b>" for i, val in enumerate(todo_obj[name][date], 1))

        await dump_todo_obj(todo_obj)
        await message.answer_sticker(skin.great.value)

        result_msg: Message = await message.answer(
            f'Вот список на этот день:\n\n{result}' if lang == 'ru' else
            f'Here is the list for this day:\n\n{result}'
        )
        if date == get_time_now(time_zone).strftime('%Y-%m-%d'):
            await dp.bot.unpin_all_chat_messages(chat_id=user_id)
            await result_msg.pin()
        else:
            date: str = (get_time_now(time_zone) + timedelta(days=1)).strftime('%Y-%m-%d')
            msg_id: int = result_msg.message_id

            scheduler.add_job(
                pin_todo_list, id=f'todo_pin_{date}{user_id}',
                args=(msg_id, user_id), trigger='date',
                replace_existing=True, run_date=date,
                misfire_grace_time=5, timezone="Europe/Moscow"
            )
    else:
        logger_guru.warning(f'{user_id=} Trying to write a message that is too large.')
        await message.answer_sticker(skin.you_were_bad.value)
        await message.answer(
            'Слишком большое сообщение ! Попробуй написать короче' if lang == 'ru' else
            'Too big message! Try to write shorter'
        )


@dp.message_handler(state='todo')
async def cancel_todo(message: Message, state: FSMContext):
    async with state.proxy() as data:
        lang: str = data['lang']
    await message.answer(
        'Тебе нужно выбрать дату :) попробуй ещё раз' if lang == 'ru' else
        'You need to choose a date :) try again'
    )
    await state.finish()
