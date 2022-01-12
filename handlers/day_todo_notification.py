from re import match as re_match

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery

from utils.keyboards.yes_no import yes_no_choice_kb
from utils.stickers_info import SendStickers
from utils.notify_users import send_todo_voice_by_ya
from loader import dp, logger_guru, scheduler
from middlewares.throttling import rate_limit




@rate_limit(5)
@dp.message_handler(Command('set_time_todo'))
async def late_day_todo_notification(message: Message, state: FSMContext):
    await message.answer('когда напоминать о делах?')
    await state.set_state('set_time_todo')
    await message.delete()


@dp.message_handler(state='set_time_todo')
async def start_weather(message: Message, state: FSMContext):
    text, user_id = ''.join(let for let in message.text if let.isnumeric()), message.from_user.id

    if re_match(r'^([01]\d|2[0-3])?([0-5]\d)$', text := text.zfill(4)[:4]):
        try:
            scheduler.add_job(send_todo_voice_by_ya, 'cron', id=f'job_send_todo_voice_by_ya_{user_id}', args=(user_id,),
                              day_of_week='mon-sun', hour=text[:2], minute=text[-2:], end_date='2023-05-30',
                              misfire_grace_time=10, replace_existing=True, timezone="Europe/Moscow")
            logger_guru.info(f"{user_id=} changed the notification time")

            await message.reply_sticker(SendStickers.great.value)
            await message.reply('Сделано !')
        except:
            logger_guru.warning(f'{user_id=} : ERROR ADD WEATHER JOB')
        finally:
            await state.finish()
    else:
        await message.reply_sticker(SendStickers.i_do_not_understand.value)
        await message.answer('Не понятно что написано, попробуй ещё раз ...')
        await state.finish()

    if not any(job.id == f'weather_add_id_{user_id}' for job in scheduler.get_jobs()):
        await message.answer('Я могу ещё писать тебе о погоде...', reply_markup=yes_no_choice_kb)


@dp.callback_query_handler(text='weather_add')
async def weather_accept(call: CallbackQuery, state: FSMContext):
    await call.message.delete_reply_markup()

    await call.message.edit_text('время?')
    await state.set_state('weather_on')