from aiogram.types import BotCommand




async def set_default_commands(dp):
    """
    Adding to the command list
    """
    await dp.bot.set_my_commands([
        BotCommand('todo','Записать "список дел"'),
        BotCommand('start_weather', 'Оповещение о погоде'),
        BotCommand('horoscope', 'Показать гороскоп'),
        BotCommand('pass', 'Записать/вспомнить пароль'),
        BotCommand('set_tntodo', 'Задать время для вечернего "брифинга"'),
        BotCommand('support', 'Help/Связаться с администрацией'),
    ])
