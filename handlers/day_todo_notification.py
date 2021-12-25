from re import match as re_match

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message

from data.stickers_info import SendStickers
from utils.notify_users import send_evening_poll
from loader import dp, logger_guru, scheduler
from middlewares.throttling import rate_limit




@rate_limit(5)
@dp.message_handler(Command('set_tntodo'))
async def late_day_todo_notification(message: Message, state: FSMContext):
    await message.answer('когда начинаем?')
    await state.set_state('set_tntodo')
    await message.delete()


@dp.message_handler(state='set_tntodo')
async def start_weather(message: Message, state: FSMContext):
    text, user_id = ''.join(let for let in message.text if let.isnumeric()), message.from_user.id

    if re_match(r'^([01]\d|2[0-3])?([0-5]\d)$', text.zfill(4)):
        try:
            scheduler.add_job(send_evening_poll, 'cron', id=f'job_evening_poll_{user_id}', args=(user_id,),
                              day_of_week='mon-sun', hour=text[:2], minute=text[-2:], end_date='2023-05-30',
                              misfire_grace_time=10, replace_existing=True, timezone="Europe/Moscow")
            logger_guru.info(f"{user_id=} changed the notification time")

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
        await message.answer('когда тебя оповещать о погоде ?')
        await state.set_state('weather_on')
