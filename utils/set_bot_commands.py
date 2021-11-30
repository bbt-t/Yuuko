from aiogram.types import BotCommand




async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        BotCommand('start', 'Запустить бота'),
        BotCommand('todo','Записать "список дел"'),
        BotCommand('start_weather', 'Оповещение о погоде'),
    ])