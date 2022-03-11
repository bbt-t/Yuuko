from asyncio import sleep as asyncio_sleep
from re import match as re_match

from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ChatActions, ContentType, CallbackQuery

from config import work_with_api
from handlers.states_in_handlers import UserSettingHandlerState
from loader import dp, scheduler, logger_guru
from utils.database_manage.sql.sql_commands import DB_USERS
from utils.misc.notify_users import send_weather
from utils.work_with_speech.speech_to_text_yandex import recognize_speech_by_ya


@dp.callback_query_handler(text='set_weather', state='settings')
async def weather_notification_on(call: CallbackQuery, state: FSMContext):
    lang, skin = await DB_USERS.select_lang_and_skin(telegram_id=call.from_user.id)

    await call.message.answer_sticker(skin.welcome.value, disable_notification=True)
    await dp.bot.send_chat_action(call.message.chat.id, ChatActions.TYPING)
    await asyncio_sleep(2)
    await call.message.answer(
        'Привет, давай я тебе помогу настроить оповещение о погоде...\n\n'
        'Напиши (или отправь голосовое сообщение) время когда тебя оповещать\n'
        'или может хочешь отменить уже заданное время?'
    )
    await call.message.delete()

    await UserSettingHandlerState.weather_on.set()
    async with state.proxy() as data:
        data['lang'] = lang


@dp.message_handler(state=UserSettingHandlerState.weather_on, content_types=[ContentType.VOICE, ContentType.TEXT])
async def start_weather(message: Message, state: FSMContext):
    async with state.proxy() as data:
        lang: str = data.get('lang')
    skin = await DB_USERS.select_skin(user_id := message.from_user.id)

    match message.content_type:
        case 'voice':
            msg: bytes = await message.bot.download_file_by_id(message.voice.file_id)
            text: str = await recognize_speech_by_ya(
                msg, work_with_api['YANDEX']['FOLDER_ID'], work_with_api['YANDEX']['API_YA_STT']
            )
        case 'text':
            text: str = message.text

    if any(text.lower().startswith(let) for let in ('отк', 'отм', 'уда')):
        try:
            scheduler.remove_job(f'weather_add_id_{user_id}')
            logger_guru.info(f"{user_id=} : turned off weather alerts")

            await message.answer('Отменено :)')
            await state.finish()
        except:
            logger_guru.exception('Error in the block of notification cancellation!')

            await message.reply_sticker(skin.hmm.value, disable_notification=True)
            await dp.bot.send_chat_action(message.chat.id, ChatActions.TYPING)
            await asyncio_sleep(1)
            await message.answer('ХММ ... не нашла записи, по-моиму ты пытаешься выключить уже выключенное.')
            await state.finish()

    elif all((
            time_text := ''.join(num for num in text if num.isnumeric()),
            re_match(r'^([01]\d|2[0-3])?([0-5]\d)$', time_text := time_text.zfill(4)[:4])
    )):
        scheduler.add_job(send_weather, 'cron', day_of_week='mon-sun', id=f'weather_add_id_{user_id}',
                          hour=time_text[:2], minute=time_text[-2:], end_date='2023-05-30', args=(user_id,),
                          misfire_grace_time=30, replace_existing=True, timezone="Europe/Moscow")

        logger_guru.info(f"{user_id=} : turned on weather notifications")
        await message.answer('ОТЛИЧНО! включили тебе поповещение о погоде :)')
        await state.finish()
    else:
        await message.reply_sticker(skin.i_do_not_understand.value, disable_notification=True)
        await message.answer('КХМ ... попробуй ещё раз ...')
        await state.finish()
