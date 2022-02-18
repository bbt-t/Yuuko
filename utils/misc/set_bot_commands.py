from aiogram.types import BotCommand, BotCommandScopeChat

from config import bot_administrators


async def set_default_commands(dp):
    """
    Adding to the command list
    """
    admin: str = bot_administrators.get('creator')

    await dp.bot.set_my_commands([
        BotCommand('todo', 'Записать "список дел"'),
        BotCommand('horoscope', 'Показать гороскоп'),
        BotCommand('hair', 'Показать дни для стрижки'),
        BotCommand('pass', 'Записать/вспомнить пароль'),
        BotCommand('set_settings', 'Настройки'),
        BotCommand('support', 'Help/Связаться с администрацией'),
        BotCommand('reset_personal_pass', 'Сбросить кодовое слово'),
    ], scope=BotCommandScopeChat(chat_id=admin, user_id=admin))

    await dp.bot.set_my_commands([
        BotCommand('todo', 'Записать "список дел"'),
        BotCommand('horoscope', 'Показать гороскоп'),
        BotCommand('hair', 'Показать дни для стрижки'),
        BotCommand('pass', 'Записать/вспомнить пароль'),
        BotCommand('set_settings', 'Настройки'),
        BotCommand('support', 'Help/Связаться с администрацией'),
    ], language_code='ru')

    await dp.bot.set_my_commands([
        BotCommand('todo', 'Write a todo list'),
        BotCommand('horoscope', 'Show horoscope'),
        BotCommand('hair', 'Show haircut days'),
        BotCommand('pass', 'Save/remember password'),
        BotCommand('set_settings', 'Settings'),
        BotCommand('support', 'Help/Contact administration'),
    ], language_code='en')

