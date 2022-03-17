from typing import Iterator, Literal

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InlineQueryResultArticle, InputTextMessageContent

from utils.getting_horoscope import get_user_horoscope_ru
from utils.misc.other_funcs import create_keyboard_button


async def choice_zodiac_keyboard(lang: str = 'ru', inline: bool = False) -> list | InlineKeyboardMarkup:
    """
    Generates keyboard for horoscope (in inline mode too).
    :param lang: language
    :param inline: for inline mode or not
    :return: list (for inline mode) or InlineKeyboard
    """
    callback_data: tuple = (
        'aries', 'taurus', 'gemini', 'cancer',
        'leo', 'virgo', 'libra', 'scorpio',
        'sagittarius', 'capricorn', 'aquarius', 'pisces',
    )
    text_ru: tuple = (
        '♈ Овен ', '♉ Телец', '♊ Близнец', '♋ Рак',
        '♌ Лев', '♍ Дева', '♎ Весы', '♏ Скорпион',
        '♐ Стрелец', '♑ Козерог', '♒ Водолей', '♓ Рыбы',
    )
    text_en: tuple = (
        '♈ Aries', '♉ Taurus', '♊ Gemini', '♋ Cancer',
        '♌ Leo', '♍ Virgo', '♎ Libra', '♏ Scorpio',
        '♐ Sagittarius', '♑ Capricorn', '♒ Aquarius', '♓ Pisces',
    )
    button_info: Iterator = map(
        lambda item: dict(zip(('text', 'callback_data'), item)),
        zip(text_ru if lang == 'ru' else text_en, callback_data)
    )
    if inline:
        return [
            InlineQueryResultArticle(
                id=f'{item.get("callback_data")}_ru',
                title=item.get("text"),
                input_message_content=InputTextMessageContent(
                    message_text=await get_user_horoscope_ru(item.get("callback_data"), 'today'))
            ) for item in button_info
        ]
    else:
        keyboard = InlineKeyboardMarkup(row_width=3)
        for info in button_info:
            keyboard.insert(InlineKeyboardButton(**info))
        return keyboard


def choice_day_zodiac_keyboard(lang: Literal['ru', 'en'] = 'ru') -> InlineKeyboardMarkup:
    """
    Generates a keyboard to select the day.
    :param lang: language
    :return: InlineKeyboard
    """
    callback_data: tuple = 'today', 'tomorrow'
    text_ru: tuple = 'на сегодня', 'на завтра'
    text_en: tuple = 'today', 'tomorrow'

    return create_keyboard_button(text=text_ru if lang == 'ru' else text_en, callback_data=callback_data)
