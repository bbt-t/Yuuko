from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from config import time_now
import handlers.todo_handl as td_h
from loader import dp, logger_guru
from utils.stickers_info import SendStickers


@dp.callback_query_handler(text='choice_del_todo')
async def inl_test_send(call: CallbackQuery, state: FSMContext):
    await call.message.delete_reply_markup()
    await call.message.answer('вышли мне их номер из списка чтобы я мог удалить.')
    await state.set_state('waiting_for_numbers_del')


@dp.message_handler(state='waiting_for_numbers_del')
async def waiting_for_del(message: Message, state: FSMContext):
    date, user_id = str(time_now.date()), message.from_user.id

    try:
        lst_for_del: list = message.text.replace(' ', '').split(',')
        for i, item in enumerate(td_h.todo_obj[f'pref_todo_{user_id}'].todo[date]):
            if i in lst_for_del:
                td_h.todo_obj[f'pref_todo_{user_id}'].todo[date].pop(i)

        await message.reply_sticker(SendStickers.great.value)
        await message.answer('Сделано!')
    except Exception as err:
        logger_guru.warning(f'{repr(err)}')
    finally:
        await state.finish()


@dp.callback_query_handler(text='delete_all_todo')
async def inl_test_send(call: CallbackQuery, state: FSMContext):
    await call.message.delete_reply_markup()
    try:
        date = str(time_now.date())
        del td_h.todo_obj[f'pref_todo_{call.from_user.id}'].todo[date]

        await call.bot.answer_callback_query(call.id, '<code>Сделано!</code> спокойной ночи :)')
    except Exception as err:
        logger_guru.warning(f'{repr(err)}')
    finally:
        await state.finish()
