from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from config import time_now
import handlers.todo_handl as td_h
from loader import bot, dp, logger_guru
from utils.keyboards.choice_del_todo_kb import choice_del__todo_keyboard




async def send_evening_poll(user_id: int):
    date = str(time_now.date())

    result = '\n'.join(f"<code>{i})</code> <b>{val}</b>" for i, val in
                       enumerate(td_h.all_todo_obj[f'pref_todo_{user_id}'].todo[date], 1))
    if result:
        await bot.send_message(user_id, f'Напоминаю что на сегодня был список \n\n{result}'
                               f'\n\nесли что-то из списка уже не актуально, можно удалить кнопкой ниже:\n',
                               reply_markup=choice_del__todo_keyboard)
    else:
        await bot.send_message(user_id, 'На сегодня ничего не было запланированно :С')


@dp.callback_query_handler(text='choice_del_todo')
async def inl_test_send(call: CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    await call.message.answer('вышли мне их номер из списка чтобы я мог удалить.')
    await state.set_state('waiting_for_numbers_del')


@dp.message_handler(state='waiting_for_numbers_del')
async def waiting_for_del(message: Message, state: FSMContext):
    date = str(time_now.date())
    user_id = message.from_user.id
    try:
        lst_for_del: list = message.text.replace(' ','').split(',')
        for i, item in enumerate(td_h.all_todo_obj[f'pref_todo_{user_id}'].todo[date]):
            if i in lst_for_del:
                td_h.all_todo_obj[f'pref_todo_{user_id}'].todo[date].pop(i)

        await message.answer('Сделано!')
    except Exception as err:
        logger_guru.warning(f'{repr(err)}')
    finally:
        await state.finish()


@dp.callback_query_handler(text='delete_all_todo')
async def inl_test_send(call: CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    try:
        date = str(time_now.date())
        del td_h.all_todo_obj[f'pref_todo_{2018211211}'].todo[date]

        await call.message.answer('<code>Сделано!</code> спокойной ночи :)')
    except Exception as err:
        logger_guru.warning(f'{repr(err)}')
    finally:
        await state.finish()
