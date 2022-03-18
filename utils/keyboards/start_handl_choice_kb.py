from typing import Literal

from aiogram.types import InlineKeyboardMarkup

from utils.misc.other_funcs import create_keyboard_button


async def get_start_keyboard(
        is_choice_skin: bool = False,
        is_set_birthday: bool = False,
        lang: Literal['ru', 'en'] = 'ru') -> InlineKeyboardMarkup:
    """
    Generates keyboards to start the bot.
    :param choice_assistant: skin selection keyboard
    :param set_birthday: to enter a date of birth
    :param lang: keyboard language
    :return: Inline keyboard
    """
    if is_choice_skin:
        callback_data: tuple = 'neko', 'chan', 'cloud'
        text_ru: tuple = 'Neko (кот)', 'Тян', 'оставить облачко'
        text_en: tuple = 'Neko (cat)', 'Chan', 'Choose a cloud'
    if is_set_birthday:
        callback_data: tuple = 'set_birthday', 'cancel'
        text_ru: tuple = 'ДАВАЙ!', 'не, может позже...'
        text_en: tuple = "LET'S!", 'no, maybe later...'

    return create_keyboard_button(text=text_ru if lang == 'ru' else text_en, callback_data=callback_data)
