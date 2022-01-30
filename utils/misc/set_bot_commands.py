from aiogram.types import BotCommand, BotCommandScopeChat

from config import admins_bot


async def set_default_commands(dp):
    """
    Adding to the command list
    """
    admin: str = admins_bot.get('creator')

    await dp.bot.set_my_commands([
        BotCommand('todo', 'Записать "список дел"'),
        BotCommand('start_weather', 'Оповещение о погоде'),
        BotCommand('horoscope', 'Показать гороскоп'),
        BotCommand('hair', 'Показать дни для стрижки'),
        BotCommand('pass', 'Записать/вспомнить пароль'),
        BotCommand('set_time_todo', 'Задать время когда напоминать о "todoшках"'),
        BotCommand('support', 'Help/Связаться с администрацией'),
        BotCommand('reset_personal_pass', 'Сбросить кодовое слово')
    ], scope=BotCommandScopeChat(chat_id=admin, user_id=admin))

    await dp.bot.set_my_commands([
        BotCommand('todo', 'Записать "список дел"'),
        BotCommand('start_weather', 'Оповещение о погоде'),
        BotCommand('horoscope', 'Показать гороскоп'),
        BotCommand('hair', 'Показать дни для стрижки'),
        BotCommand('pass', 'Записать/вспомнить пароль'),
        BotCommand('set_time_todo', 'Задать время когда напоминать о "todoшках"'),
        BotCommand('support', 'Help/Связаться с администрацией'),
    ], language_code='ru')

    await dp.bot.set_my_commands([
        BotCommand('todo', 'Write a todo list'),
        BotCommand('start_weather', 'Weather alert'),
        BotCommand('horoscope', 'Show horoscope'),
        BotCommand('hair', 'Show haircut days'),
        BotCommand('pass', 'Save/remember password'),
        BotCommand('set_time_todo', 'Set the time when to remind about "todos"'),
        BotCommand('support', 'Help/Contact administration'),
    ], language_code='en')

