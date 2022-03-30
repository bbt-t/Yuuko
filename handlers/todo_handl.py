from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery

from config import bot_config
from loader import dp, logger_guru, scheduler
from .states_in_handlers import TodoStates
from middlewares.throttling import rate_limit
from utils.database_manage.sql.sql_commands import DB_USERS
from utils.keyboards.calendar import calendar_bot_en, calendar_bot_ru, CalendarBot
from utils.misc.other_funcs import get_time_now
from utils.todo import load_todo_obj, dump_todo_obj, pin_todo_message


@rate_limit(2, key='todo')
@dp.message_handler(Command('todo'))
async def bot_todo(message: Message, state: FSMContext):
    lang, skin = await DB_USERS.select_lang_and_skin(telegram_id=message.from_user.id)

    await message.answer_sticker(skin.love_you.value, disable_notification=True)
    if lang == 'ru':
        await message.answer(
            '<code>Привет! :)\nдавай запишем что сделать и когда</code>',
            reply_markup=calendar_bot_ru.enable())
    else:
        await message.answer(
            '<code>Привет! :)\nдавай запишем что сделать и когда</code>',
            reply_markup=calendar_bot_en.enable())

    await TodoStates.first()
    async with state.proxy() as data:
        data['lang'] = lang

    await message.delete()


@dp.callback_query_handler(CalendarBot.callback.filter(), state=TodoStates.todo)
async def process_simple_calendar(call: CallbackQuery, callback_data, state: FSMContext) -> None:
    async with state.proxy() as data:
        lang: str = data.get('lang')
    selected, date = (await calendar_bot_ru.process_selection(call, callback_data) if lang == 'ru' else
                      await calendar_bot_en.process_selection(call, callback_data))

    if date and selected:
        if date < get_time_now(bot_config.time_zone).date():
            if lang == 'ru':
                await call.answer('Выбрать можно только на сегодня и позже !', show_alert=True)
                await call.message.answer(
                    'Ты не можешь выбрать эту дату!', reply_markup=calendar_bot_ru.enable()
                )
            else:
                await call.answer('You can only choose today and later!', show_alert=True)
                await call.message.answer(
                    "You can't choose this date!", reply_markup=calendar_bot_ru.enable()
                )
        else:
            async with state.proxy() as data:
                data['date'] = str(date)

            await call.message.edit_text(
                f'Что планируешь на <code>{date}</code> число?' if lang == 'ru' else
                f'What are you planning for the <code>{date}</code>?'
            )
            await TodoStates.next()


@dp.message_handler(state=TodoStates.reception_todo)
async def set_calendar_date(message: Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        lang, date = data.values()

    user_id: int = message.from_user.id
    name, skin = f'todo_{user_id}', await DB_USERS.select_skin(telegram_id=user_id)

    if len(message.text) <= 1000:
        message_task: list = [item for item in message.text.split('\n') if item]
        todo_obj: dict = await load_todo_obj()
        try:
            todo_obj.setdefault(name, {})[date].extend(message_task)
        except KeyError:
            todo_obj[name].setdefault(date, message_task)
        else:
            await dump_todo_obj(todo_obj)
        finally:
            await dump_todo_obj(todo_obj)
            await message.delete()
            await state.finish()

        result: str = '\n'.join(f"<code>{i})</code> <b>{val}</b>" for i, val in enumerate(todo_obj[name][date], 1))

        await message.answer_sticker(skin.great.value, disable_notification=True)
        send_msg: Message = await message.answer(
            f'Вот список на этот день:\n\n{result}' if lang == 'ru' else
            f'Here is the list for this day:\n\n{result}'
        )
        if date == get_time_now(bot_config.time_zone).strftime('%Y-%m-%d'):
            await dp.bot.unpin_all_chat_messages(chat_id=user_id)
            await send_msg.pin(disable_notification=True)
        else:
            scheduler.add_job(
                func=pin_todo_message,
                args=(message.chat.id, user_id),
                trigger='date',
                id=f'{user_id}_pin_msg_job',
                run_date=f'{date} 00:05:05',
                misfire_grace_time=5,
                replace_existing=True,
                timezone="Europe/Moscow"
            )
    else:
        logger_guru.warning(f'{user_id=} Trying to write a message that is too large.')
        await message.answer_sticker(skin.you_were_bad.value, disable_notification=True)
        await message.answer(
            'Слишком большое сообщение ! Попробуй написать короче...' if lang == 'ru' else
            'Too big message! Try to write shorter'
        )


@dp.message_handler(state=TodoStates.todo)
async def cancel_todo(message: Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        lang: str = data['lang']

    await message.answer(
        'Тебе нужно выбрать дату :) попробуй ещё раз!' if lang == 'ru' else
        'You need to choose a date :) try again!'
    )
    await state.finish()
