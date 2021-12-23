from aiogram.types import BotCommand




async def set_default_commands(dp):
    """
    Adding to the command list
    """
    await dp.bot.set_my_commands([
        BotCommand('todo','Записать "список дел"'),
        BotCommand('start_weather', 'Оповещение о погоде'),
        BotCommand('horoscope', 'показать гороскоп'),
        BotCommand('pass', 'Записать/вспомнить пароль'),
        BotCommand('support', 'Help/Связаться с администрацией'),
    ])