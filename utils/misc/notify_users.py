from functools import wraps

from aiogram.types import ParseMode, Message

from config import work_with_api, time_zone
from loader import dp, logger_guru, get_time_now
from ..database_manage.sql.sql_commands import select_user
from ..todo import load_todo_obj
from ..weather_compilation import create_weather_forecast
from ..work_with_speech.text_to_speech_yandex import synthesize_voice_by_ya




def auth(func):
    """
    Wrap for check user
    :param func: handler
    :return: message or None
    """
    @wraps(func)
    async def wrapper(message: Message):
        if message.from_user.is_bot:
            logger_guru.critical(f'{message.from_user.id=} : Bot is trying to log-in!')
            return None
        if await select_user(id=message.from_user.id):
            await message.delete()
            return await message.reply('Мы же уже знакомы :)', reply=False)
        return await func(message)
    return wrapper


@logger_guru.catch()
async def send_weather(id: int):
    """
    Sends a message with the weather
    :param id: user id
    :return: message
    """
    text_msg: str = await create_weather_forecast()
    await dp.bot.send_message(id, text_msg, ParseMode.HTML)


@logger_guru.catch()
async def send_synthesize_voice_by_ya(
        id: int, text: str, lang: str,
        folder: str = work_with_api['YANDEX']['FOLDER_ID'],
        api_ya_tts: str = work_with_api['YANDEX']['API_YA_TTS']):
    """
    Sends a message with the synthesize voice message
    :param id: user id
    :param text: text for synthesis
    :param: folder: your cloud name Yandex
    :param: api_ya_tts: api-key
    :return: voice message
    """
    text_msg: bytes = await synthesize_voice_by_ya(folder, api_ya_tts, text, lang)
    await dp.bot.send_voice(id, text_msg)


@logger_guru.catch()
async def send_todo_msg(
        user_id: int | str, is_voice: bool = False,
        folder: str = work_with_api['YANDEX']['FOLDER_ID'],
        api_ya_tts: str = work_with_api['YANDEX']['API_YA_TTS']
        ):
    """
    Sends a message with the synthesize voice message
    :param user_id: telegram id of the person to whom the message will be sent
    :param is_voice: send voice message or not
    :param: folder: your cloud name Yandex
    :param: api_ya_tts: api-key
    :return: voice message and text message
    """
    name, date = f'todo_{user_id}', get_time_now(time_zone).strftime('%Y-%m-%d')

    try:
        todo_obj: dict = await load_todo_obj()
        text_msg: str = '\n\n'.join(f"{i}. {val}" for i, val in enumerate(todo_obj[name][str(date)], 1))

        if is_voice:
            voice_msg: bytes = await synthesize_voice_by_ya(
                folder, api_ya_tts,
                f"Привет! Напоминаю что на сегодня список дел таков: {text_msg}"
            )
            await dp.bot.send_voice(user_id, voice_msg)

        await dp.bot.send_message(user_id, f'Напоминаю что на сегодня список дел таков: \n\n{text_msg}')

    except Exception as err:
        logger_guru.warning(f"{repr(err)} : {user_id}")
        await dp.bot.send_message(user_id, 'На сегодня ничего не было запланированно :С')
