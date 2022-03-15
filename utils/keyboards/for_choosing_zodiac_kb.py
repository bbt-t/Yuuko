from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InlineQueryResultArticle, InputTextMessageContent

from utils.getting_horoscope import get_user_horoscope_ru
from typing import Iterator


async def choice_zodiac_keyboard(lang: str = 'ru', inline: bool = False) -> list | InlineKeyboardMarkup:
    """
    Generates keyboard for horoscope (in inline mode too).
    :param lang: language
    :param inline: for inline mode or not
    :return: list (for inline mode) or InlineKeyboard
    """
    zodiac_ru: tuple = (
        ('♈ Овен ', 'aries'),
        ('♉ Телец', 'taurus'),
        ('♊ Близнец', 'gemini'),
        ('♋ Рак', 'cancer'),
        ('♌ Лев', 'leo'),
        ('♍ Дева', 'virgo'),
        ('♎ Весы', 'libra'),
        ('♏ Скорпион', 'scorpio'),
        ('♐ Стрелец', 'sagittarius'),
        ('♑ Козерог', 'capricorn'),
        ('♒ Водолей', 'aquarius'),
        ('♓ Рыбы', 'pisces'),
    )
    zodiac_en: tuple = (
        ('♈ Aries', 'aries'),
        ('♉ Tauru', 'taurus'),
        ('♊ Gemini', 'gemini'),
        ('♋ Cancer', 'cancer'),
        ('♌ Leo', 'leo'),
        ('♍ Virgo', 'virgo'),
        ('♎ Libra', 'libra'),
        ('♏ Scorpio', 'scorpio'),
        ('♐ Sagittarius', 'sagittarius'),
        ('♑ Capricorn', 'capricorn'),
        ('♒ Aquarius', 'aquarius'),
        ('♓ Pisces', 'pisces'),
    )
    button_info: Iterator[dict] = map(
        lambda item: dict(zip(('text', 'callback_data'), item)),
        zodiac_ru if lang == 'ru' else zodiac_en
    )
    if inline:
        return [
            InlineQueryResultArticle(
                id=f'{x.get("callback_data")}_ru',
                title=x.get("text"),
                input_message_content=InputTextMessageContent(
                    message_text=await get_user_horoscope_ru(x.get("callback_data"), 'today'))
            ) for x in button_info
        ]
    else:
        keyboard = InlineKeyboardMarkup(row_width=3)
        for info in button_info:
            keyboard.insert(InlineKeyboardButton(**info))
        return keyboard


async def choice_day_zodiac_keyboard(lang: str = 'ru') -> InlineKeyboardMarkup:
    """
    Generates a keyboard to select the day.
    :param lang: language
    :return: InlineKeyboard
    """
    day_ru: tuple = (
        ('на сегодня', 'today'),
        ('на завтра', 'tomorrow'),
    )
    day_en: tuple = (
        ('на сегодня', 'today'),
        ('на завтра', 'tomorrow'),
    )
    button_info: Iterator[dict] = map(
        lambda item: dict(zip(('text', 'callback_data'), item)),
        day_ru if lang == 'ru' else day_en
    )
    keyboard = InlineKeyboardMarkup(row_width=2)
    for info in button_info:
        keyboard.insert(InlineKeyboardButton(**info))
    return keyboard
