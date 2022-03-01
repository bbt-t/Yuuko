from functools import wraps
from time import sleep

from aiogram.types import ParseMode, Message
from aiogram.utils.exceptions import BotBlocked

from config import work_with_api, time_zone
from loader import dp, logger_guru
from .other_funcs import get_time_now
from ..database_manage.sql.sql_commands import select_user, select_all_users
from ..todo import load_todo_obj, pin_todo_message
from ..weather_compilation import create_weather_forecast
from ..work_with_speech.text_to_speech_yandex import synthesize_voice_by_ya


def auth(func) -> Message | None:
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
        if await select_user(telegram_id=message.from_user.id):
            await message.delete()
            return await message.answer(
                'Мы же уже знакомы :)' if message.from_user.language_code == 'ru' else
                'We are already familiar', reply=False
            )
        return await func(message)
    return wrapper


@logger_guru.catch()
async def send_weather(telegram_id: int) -> None:
    """
    Sends a message with the weather
    :param telegram_id: user id
    :return: message
    """
    text_msg: str = await create_weather_forecast()
    await dp.bot.send_message(telegram_id, text_msg, ParseMode.HTML)


@logger_guru.catch()
async def send_synthesize_voice_by_ya(
        telegram_id: int | str, text: str, lang: str,
        folder: str = work_with_api['YANDEX']['FOLDER_ID'],
        api_ya_tts: str = work_with_api['YANDEX']['API_YA_TTS']) -> None:
    """
    Sends a message with the synthesize voice message
    :param telegram_id: user id
    :param text: text for synthesis
    :param: folder: your cloud name Yandex
    :param: api_ya_tts: api-key
    :return: voice message
    """
    text_msg: bytes = await synthesize_voice_by_ya(folder, api_ya_tts, text, lang)
    await dp.bot.send_voice(telegram_id, text_msg)


async def send_todo_msg(
        telegram_id: int | str, is_voice: bool = False,
        folder: str = work_with_api['YANDEX']['FOLDER_ID'],
        api_ya_tts: str = work_with_api['YANDEX']['API_YA_TTS']
        ) -> None:
    """
    Sends a message with the synthesize voice message
    :param telegram_id: telegram id of the person to whom the message will be sent
    :param is_voice: send voice message or not
    :param: folder: your cloud name Yandex
    :param: api_ya_tts: api-key
    :return: voice message and text message
    """
    name, date = f'todo_{telegram_id}', get_time_now(time_zone).strftime('%Y-%m-%d')

    try:
        todo_obj: dict = await load_todo_obj()
        text_msg: str = '\n\n'.join(f"{i}. {val}" for i, val in enumerate(todo_obj[name][date], 1))

        if is_voice:
            voice_msg: bytes = await synthesize_voice_by_ya(
                folder, api_ya_tts,
                f"Привет! Напоминаю что на сегодня список дел таков: {text_msg}",
                lang='ru'
            )
            await dp.bot.send_voice(telegram_id, voice_msg)
        await dp.bot.send_message(telegram_id, f'Cписок дел на сегодня: \n\n{text_msg}')
    except Exception as err:
        logger_guru.warning(f"{repr(err)} : {telegram_id=}")
        await dp.bot.send_message(telegram_id, 'На сегодня ничего не было запланированно 🥱')
        await dp.bot.unpin_all_chat_messages(chat_id=telegram_id)


async def send_a_message_to_all_users(msg: str) -> None | str:
    """
    When sending notifications to multiple users,
    the API will not allow sending more than 30 messages per second.
    :param msg: text to send
    :return: None if everything went well, else user id that caused the error
    """
    counter: int = 0
    for telegram_id in await select_all_users():
        try:
            if counter < 20:
                await dp.bot.send_message(chat_id=telegram_id, text=msg)
                counter += 1
            else:
                sleep(1)
                counter = 0
        except BotBlocked:
            logger_guru.warning(f'{telegram_id} : error when trying to send')
            return f'mistakes: {telegram_id}'

