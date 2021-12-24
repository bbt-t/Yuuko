from functools import wraps

from aiogram.types import ParseMode, Message

from config import API_WEATHER, API_WEATHER2, FOLDER_ID, API_YA_TTS, CITY_WEATHER, time_now
from loader import bot, logger_guru
from utils.db_api.sql_commands import select_user
from utils.keyboards.choice_del_todo_kb import choice_del_todo_keyboard
from utils.weather_compilation import create_weather_forecast
from utils.work_with_speech.text_to_speech_yandex import synthesize_voice_by_ya
from handlers.todo_handl import all_todo_obj




def auth(func):
    """
    Wrap for check user
    :param func: handler
    :return: message or None
    """
    @wraps(func)
    async def wrapper(message: Message):
        if await select_user(id=message.from_user.id):
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
    text_msg = await create_weather_forecast(API_WEATHER, API_WEATHER2, city)
    await bot.send_message(id, text_msg, ParseMode.HTML)


@logger_guru.catch()
async def send_synthesize_voice_by_ya(id: int, text: str):
    """
    Sends a message with the synthesize voice message
    :param id: user id
    :param text: text for synthesis
    :return: voice message
    """
    text_msg = await synthesize_voice_by_ya(FOLDER_ID, API_YA_TTS, text)
    await bot.send_voice(id, text_msg)


@logger_guru.catch()
async def send_todo_voice_by_ya():
    """
    Sends a message with the synthesize voice message
    :return: voice message and text message
    """
    date: str = str(time_now.date())

    for item in all_todo_obj.values():
        for key in item.todo:
            if key == date:
                msg_from_todo: str = '\n'.join(f"{i}. {val}." for i, val in enumerate(item.todo[key], 1))
                msg: str = f'На сегодня у тебя запланированно:\n{msg_from_todo}'
                await bot.send_voice(item.id, synthesize_voice_by_ya(FOLDER_ID, API_YA_TTS, msg))
                await bot.send_message(item.id, msg)


async def send_evening_poll(user_id: int):
    date = str(time_now.date())

    result: str = '\n'.join(f"<code>{i})</code> <b>{val}</b>" for i, val in
                       enumerate(td_h.all_todo_obj[f'pref_todo_{user_id}'].todo[date], 1))
    if result:
        await bot.send_message(user_id, f'Напоминаю что на сегодня был список \n\n{result}'
                               f'\n\nесли что-то из списка уже не актуально, можно удалить кнопкой ниже:\n',
                               reply_markup=choice_del_todo_keyboard)
    else:
        await bot.send_message(user_id, 'На сегодня ничего не было запланированно :С')