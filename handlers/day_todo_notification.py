from re import match

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message

from handlers.question_at_the_end_day import send_evening_poll
from loader import dp, logger_guru, scheduler, db
from middlewares.throttling import rate_limit




@rate_limit(5)
@dp.message_handler(Command('set_tntodo'))
async def late_day_todo_notification(message: Message, state: FSMContext):
    await message.answer('Чтобы задать время для вечернего "брифинга" введи\n')
    await state.set_state('set_tntodo')


@dp.message_handler(state='set_tntodo')
async def start_weather(message: Message, state: FSMContext):
    text: str = message.text.lower().replace(' ', '')
    user_id: int = message.from_user.id

    if match(r'^([01]\d|2[0-3]):?([0-5]\d)$', text):
        try:
            scheduler.add_job(send_evening_poll, 'cron', id=f'job_evening_poll_{user_id}', args=(user_id,),
                              day_of_week='mon-sun', hour=text[:2], minute=text[-2:], end_date='2023-05-30',
                              misfire_grace_time=10, replace_existing=True, timezone="Europe/Moscow")
            logger_guru.info(f"{user_id=} changed the notification time")

            await message.answer('Сделано !')
        except:
            logger_guru.warning(f'{user_id=} : ERROR ADD WEATHER JOB')
        finally:
            await state.finish()
    else:
        await message.answer('Не распознал что написано, попробуй ещё раз ...')
        await state.finish()

    if user_id not in db.select_all_users_weather():
        await message.answer('когда тебя оповещать о погоде ?')
        await state.set_state('weather_on')