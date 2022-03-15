from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InlineQueryResultArticle, InputTextMessageContent

from utils.getting_horoscope import get_user_horoscope_ru
from typing import Iterator


async def choice_zodiac_keyboard(lang: str = 'ru', inline: bool = False) -> list | InlineKeyboardMarkup:
    """

    :param lang:
    :param inline:
    :return:
    """
    zodiac_ru = (
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
    zodiac_en = (
        ('♈ Aries 21 March – 20 April', 'aries'),
        ('♉ Taurus 21 April – 20 May', 'taurus'),
        ('♊ Gemini 21 May – 21 June', 'gemini'),
        ('♋ Cancer 22 June – 22 July', 'cancer'),
        ('♌ Leo 23 July – 23 August', 'leo'),
        ('♍ Virgo 24 August – 23 September', 'virgo'),
        ('♎ Libra 24 September – 23 October', 'libra'),
        ('♏ Scorpio 24 October – 22 November', 'scorpio'),
        ('♐ Sagittarius 23 November – 21 December', 'sagittarius'),
        ('♑ Capricorn 22 December – 20 January', 'capricorn'),
        ('♒ Aquarius 21 January – 20 February', 'aquarius'),
        ('♓ Pisces 21 February – 20 March', 'pisces'),
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

    :param lang:
    :return:
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

