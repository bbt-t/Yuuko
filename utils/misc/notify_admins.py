from aiogram import Dispatcher

from config import bot_config
from loader import logger_guru


async def on_startup_notify(dp: Dispatcher) -> None:
    """
    Newsletter to admins when the bot is started
    """
    try:
        await dp.bot.send_message(bot_config.bot_administrators.creator, 'Бот запущен')
    except Exception as err:
        logger_guru.warning(f'{repr(err)} : Сan not send a message to the administrator')


async def on_shutdown_notify(dp: Dispatcher) -> None:
    """
    Newsletter to admins when the bot is stopped
    """
    try:
        await dp.bot.send_message(bot_config.bot_administrators.creator, 'Бот остановлен!')
    except Exception as err:
        logger_guru.warning(f'{repr(err)} : Сan not send a message to the administrator')
