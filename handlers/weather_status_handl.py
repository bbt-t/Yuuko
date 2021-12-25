from asyncio import sleep as asyncio_sleep
from re import match as re_match
from sqlite3 import Error as sqlite3_Error

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import Command
from aiogram.types import Message, ChatActions, ContentType
from apscheduler.jobstores.base import JobLookupError

from config import FOLDER_ID, API_YA_STT
from data.stickers_info import SendStickers
from loader import dp, bot, scheduler, logger_guru
from middlewares.throttling import rate_limit
from utils.notify_users import send_weather
from utils.work_with_speech.speech_to_text_yandex import recognize_speech_by_ya




@rate_limit(5)
@dp.message_handler(Command('start_weather'))
async def weather_notification_on(message: Message, state: FSMContext):
    await message.answer_sticker('CAACAgIAAxkBAAEDZZZhp4UKWID3NNoRRLywpZPBSmpGUwACVwEAAhAabSKlKzxU-3o0qiIE')
    await bot.send_chat_action(message.chat.id, ChatActions.TYPING)
    await asyncio_sleep(2)
    await message.answer('Привет, давай я тебе помогу настроить оповещение о погоде...\n\n'
                         'Напиши (или отправь голосовое сообщение) время когда тебя оповещать\n'
                         'или может хочешь отменить уже заданное время?')
    await state.set_state('weather_on')
    await message.delete()


@dp.message_handler(state='weather_on', content_types=[ContentType.VOICE, ContentType.TEXT])
async def start_weather(message: Message, state: FSMContext):
    user_id: int = message.from_user.id
    match message.content_type:
        case 'voice':
            msg: bytes = await message.bot.download_file_by_id(message.voice.file_id)
            text: str = await recognize_speech_by_ya(msg, FOLDER_ID, API_YA_STT)
        case 'text':
            text = message.text

    if any(
            let.lower().startswith(x) for let in text.split()
            for x in ('отм', 'вык', 'уда', 'да') if not let.isnumeric()
    ):
        try:
            scheduler.remove_job(f'weather_add_id_{user_id}')
            logger_guru.info(f"{user_id=} : turned off weather alerts")

            await message.answer('Отменено :)')
            await state.finish()
        except (sqlite3_Error, JobLookupError) as err:
            logger_guru.warning(f'{repr(err)} : Error in the block of notification cancellation!')

            await message.reply_sticker(SendStickers.hmm.value)
            await bot.send_chat_action(message.chat.id, ChatActions.TYPING)
            await asyncio_sleep(1)
            await message.answer('ХММ ... не нашла записи, по-моиму ты пытаешься выключить уже выключенное.')
            await state.finish()

    elif re_match(r'^([01]\d|2[0-3])?([0-5]\d)$', ''.join(num for num in text if num.isnumeric()).replace(' ', '')):

            scheduler.add_job(send_weather, 'cron', day_of_week='mon-sun', id=f'weather_add_id_{user_id}',
                              hour=text[:2], minute=text[-2:], end_date='2023-05-30', args=(user_id,),
                              misfire_grace_time=30,replace_existing=True, timezone="Europe/Moscow")

            logger_guru.info(f"{user_id=} : turned on weather notifications")
            await message.answer('ОТЛИЧНО! включили тебе поповещение о погоде :)')
            await state.finish()
    else:
        await message.reply_sticker(SendStickers.i_do_not_understand.value)
        await message.answer('КХМ ... попробуй ещё раз ...')
        await state.finish()