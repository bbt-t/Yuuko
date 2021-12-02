from asyncio import sleep
from re import match
from sqlite3 import Error

from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ChatActions
from aiogram.dispatcher.filters.builtin import Command
from apscheduler.jobstores.base import JobLookupError

from loader import dp, db, scheduler, logger_guru, bot
from utils.notify_users import send_weather
from middlewares.throttling import rate_limit




@rate_limit(5)
@dp.message_handler(Command('start_weather'))
async def weather_notification_on(message: Message, state: FSMContext):
    await bot.send_chat_action(message.chat.id, ChatActions.TYPING)
    await sleep(2)
    await message.answer('Привет, давай я тебе помогу настроить оповещение о погоде...\n\n'
                         'Напиши время когда тебя оповещать\n\n'
                         'или, если хочешь отменить уже заданное время --->  <CODE>ОТМЕНИТЬ</CODE>\n')
    await state.set_state('weather_on')


@dp.message_handler(state='weather_on')
async def start_weather(message: Message, state: FSMContext):

    user_id: int = message.from_user.id
    if any((item.startswith(let) for item in message.text) for let in ('отм', 'вык', 'уда')):
        try:
            db.update_weather_status(user_id, None)
            scheduler.remove_job(f'weather_add_id_{user_id}')
            logger_guru.info(f"{user_id=} : turned off weather alerts")

            await message.answer('Отменено :)')
            await state.finish()
        except (Error, JobLookupError) as err:
            logger_guru.warning(f'{repr(err)} : Error in the block of notification cancellation!')

            await message.reply('Не нашла записи, по-моиму ты пытаешься выключить уже выключенное.')
            await state.finish()

    elif match(r'^([01]\d|2[0-3])?([0-5]\d)$', text):
        try:
            db.update_weather_status(user_id, text)
            scheduler.add_job(send_weather, 'cron', day_of_week='mon-sun', id=f'weather_add_id_{user_id}',
                              hour=text[:2], minute=text[-2:], end_date='2023-05-30', args=(user_id,),
                              misfire_grace_time=30,replace_existing=True, timezone="Europe/Moscow")
        except:
            logger_guru.warning(f'{user_id=} : ERROR ADD WEATHER JOB')
        else:
            logger_guru.info(f"{user_id=} : turned on weather notifications")
            await bot.answer_callback_query('ОТЛИЧНО! включили тебе поповещение о погоде :)')
            await state.finish()
    else:
        await message.reply_sticker('CAACAgIAAxkBAAEDZaFhp4qDluGGvnCQe2WhofQ3r2wtfgACrAEAAhAabSJ41lvmGuTmxyIE')
        await message.answer('КХМ ... попробуй ещё раз ...')
        await state.finish()