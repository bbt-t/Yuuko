from aiogram.types import BotCommand, BotCommandScopeChat

from config import bot_config


async def set_default_commands(dp) -> None:
    """
    Adding to the command list
    """
    admin: str = bot_config.bot_administrators.creator

    await dp.bot.set_my_commands([
        BotCommand('todo', 'Записать "список дел"'),
        BotCommand('horoscope', 'Показать гороскоп'),
        BotCommand('hair', 'Показать дни для стрижки'),
        BotCommand('pass', 'Записать/вспомнить пароль'),
        BotCommand('recipe', 'Записать/вспомнить рецепт'),
        BotCommand('set_settings', 'Настройки'),
        BotCommand('support', 'Help/Связаться с администрацией'),
        BotCommand('admin_tools', 'администратору'),
    ], scope=BotCommandScopeChat(chat_id=admin, user_id=admin))

    await dp.bot.set_my_commands([
        BotCommand('todo', 'Записать "список дел"'),
        BotCommand('horoscope', 'Показать гороскоп'),
        BotCommand('hair', 'Показать дни для стрижки'),
        BotCommand('pass', 'Записать/вспомнить пароль'),
        BotCommand('recipe', 'Записать/вспомнить рецепт'),
        BotCommand('set_settings', 'Настройки'),
        BotCommand('support', 'Help/Связаться с администрацией'),
    ], language_code='ru')

    await dp.bot.set_my_commands([
        BotCommand('todo', 'Write a todo list'),
        BotCommand('horoscope', 'Show horoscope'),
        BotCommand('hair', 'Show haircut days'),
        BotCommand('pass', 'Save/remember password'),
        BotCommand('recipe', 'Save/remember recipe'),
        BotCommand('set_settings', 'Settings'),
        BotCommand('support', 'Help/Contact administration'),
    ], language_code='en')
