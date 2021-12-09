from functools import wraps

from aiogram.types import ParseMode, Message

from config import API_WEATHER, API_WEATHER2, FOLDER_ID, API_YA_TTS, CITY_WEATHER
from loader import bot, db, logger_guru
from utils.weather_compilation import create_weather_forecast
from utils.work_with_speech.text_to_speech_yandex import synthesize_voice_by_ya



def auth(func):
    """
    Wrap for check user
    :param func: handler
    :return: message or None
    """
    @wraps(func)
    async def wrapper(message: Message):
        if db.select_user(telegram_id=message.from_user.id):
            await message.delete()
            return await message.reply('Мы же уже знакомы :)', reply=False)
        return await func(message)
    return wrapper


@logger_guru.catch()
async def send_weather(id: int, city: str = CITY_WEATHER):
    """
    Sends a message with the weather
    :param city: city
    :param id: user id
    :return: message
    """
    await bot.send_message(id, create_weather_forecast(API_WEATHER, API_WEATHER2, city), ParseMode.HTML)


@logger_guru.catch()
async def send_synthesize_voice_by_ya(id: int, text: str):
    """
    Sends a message with the synthesize voice message
    :param id: user id
    :param text: text for synthesis
    :return: voice message
    """
    await bot.send_voice(id, synthesize_voice_by_ya(FOLDER_ID, API_YA_TTS, text))