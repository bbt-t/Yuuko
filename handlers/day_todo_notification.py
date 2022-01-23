from re import match as re_match

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery

from loader import dp, logger_guru, scheduler
from middlewares.throttling import rate_limit
from utils.keyboards.choice_voice_todo import choice_voice_todo_keyboard
from utils.keyboards.yes_no import yes_no_choice_kb
from utils.misc.notify_users import send_todo_msg
from utils.misc.enums_data import SendStickers




@rate_limit(5)
@dp.message_handler(Command('set_time_todo'))
async def late_day_todo_notification(message: Message, state: FSMContext):
    await message.answer('когда напоминать о делах?')
    await state.set_state('set_time_todo')
    await message.delete()


@dp.message_handler(state='set_time_todo')
async def question_set_time_todo(message: Message, state: FSMContext):
    await message.answer_sticker(SendStickers.love_you.value)
    await message.answer('а можно я тебе буду голосовые сообщения слать?', reply_markup=choice_voice_todo_keyboard)
    await state.set_data(message.text)


@dp.callback_query_handler(state='set_time_todo')
async def start_set_time_todo(call: CallbackQuery, state: FSMContext):
    await call.message.delete_reply_markup()

    msg, choice, user_id = await state.get_data(), call.data, call.from_user.id
    text: str = ''.join(let for let in msg if let.isnumeric())

    if re_match(r'^([01]\d|2[0-3])?([0-5]\d)$', text := text.zfill(4)[:4]):
        try:
            is_voice = True if choice != 'choice_voice_no' else False

            scheduler.add_job(send_todo_msg, 'cron', day_of_week='mon-sun', id=f'job_send_todo_{user_id}',
                              hour=text[:2], minute=text[-2:], end_date='2025-05-30', args=(user_id, is_voice),
                              misfire_grace_time=30, replace_existing=True, timezone="Europe/Moscow")

            logger_guru.info(f"{user_id=} changed the notification time")
            await call.message.answer_sticker(SendStickers.great.value)
            await call.message.answer('Сделано !')
        except:
            logger_guru.warning(f'{user_id=} : ERROR ADD WEATHER JOB')
        finally:
            await state.finish()
    else:
        await call.message.answer_sticker(SendStickers.i_do_not_understand.value)
        await call.message.answer('Не понятно что написано, попробуй ещё раз ...')
        await state.finish()

    if not any(job.id == f'weather_add_id_{user_id}' for job in scheduler.get_jobs()):
        await call.message.answer('Я могу ещё писать тебе о погоде...', reply_markup=yes_no_choice_kb)


@dp.callback_query_handler(text='weather_add')
async def weather_accept(call: CallbackQuery, state: FSMContext):
    await call.message.delete_reply_markup()

    await call.message.edit_text('время?')
    await state.set_state('weather_on')