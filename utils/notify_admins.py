from loader import logger_guru
from config import AdminsBot




async def on_startup_notify(dp):
    """
    Рассылка админам при запуске бота
    """
    try:
        await dp.bot.send_message(AdminsBot.creator.value, 'Бот запущен')
    except Exception as err:
        logger_guru.warning(f'{repr(err)} : Сan not send a message to the administrator')

async def on_shutdown_notify(dp):
    """
    Рассылка админам при остановке бота
    """
    try:
        await dp.bot.send_message(AdminsBot.creator.value, 'Бот остановлен!')
    except Exception as err:
        logger_guru.warning(f'{repr(err)} : Сan not send a message to the administrator')