from functools import wraps

from aiogram.types import ParseMode, Message

from config import API_WEATHER, API_WEATHER2, CITY_WEATHER, time_now, FOLDER_ID, API_YA_TTS
from loader import dp, logger_guru
from .db_api.sql_commands import select_user
from .todo import load_todo_obj
from .weather_compilation import create_weather_forecast
from .work_with_speech.text_to_speech_yandex import synthesize_voice_by_ya




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
async def send_weather(id: int, api: str=API_WEATHER, api2: str=API_WEATHER2, city: str = CITY_WEATHER):
    """
    Sends a message with the weather
    :param city: city
    :param id: user id
    :return: message
    """
    text_msg: str = await create_weather_forecast(api, api2, city)
    await dp.bot.send_message(id, text_msg, ParseMode.HTML)


@logger_guru.catch()
async def send_synthesize_voice_by_ya(id: int, text: str, folder=FOLDER_ID, api_ya_tts: str=API_YA_TTS):
    """
    Sends a message with the synthesize voice message
    :param id: user id
    :param text: text for synthesis
    :return: voice message
    """
    text_msg: bytes = await synthesize_voice_by_ya(folder, api_ya_tts, text)
    await dp.bot.send_voice(id, text_msg)


@logger_guru.catch()
async def send_todo_msg(user_id: int | str, is_voice: bool = False, folder: str=FOLDER_ID, api_ya_tts: str=API_YA_TTS):
    """
    Sends a message with the synthesize voice message
    :param user_id: telegram id of the person to whom the message will be sent
    :param is_voice: send voice message or not
    :return: voice message and text message
    """
    date, name = str(time_now.date()), f'todo_{user_id}'

    try:
        todo_obj: dict = await load_todo_obj()
        text_msg: str = '\n\n'.join(f"{i}. {val}" for i, val in enumerate(
            todo_obj[name][date], 1)
                               )
        try:
            if is_voice:
                voice_msg: bytes = await synthesize_voice_by_ya(
                    folder, api_ya_tts,
                    f"Привет! Напоминаю что на сегодня список дел таков: {text_msg}"
                )
                await dp.bot.send_voice(user_id, voice_msg)
        except:
            logger_guru.warning('ERROR IN VOICE API REQ')
        await dp.bot.send_message(user_id, f'Напоминаю что на сегодня список дел таков: \n\n{text_msg}')

    except Exception as err:
        logger_guru.warning(f"{repr(err)} : {user_id}")
        await dp.bot.send_message(user_id, 'На сегодня ничего не было запланированно :С')
