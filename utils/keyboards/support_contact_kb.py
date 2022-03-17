from typing import Optional

from aiogram.utils.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import bot_administrators


sup_cb = CallbackData('sup_ask', 'telegram_id')


async def sup_kb(telegram_id: Optional[int] = None) -> InlineKeyboardMarkup:
    """
    Keyboard for feedback with the administration.
    :param telegram_id: user id
    :return: shaped inline-keyboard
    """
    if telegram_id:
        contact: int = telegram_id
        text: str = 'Ответить пользователю'
    else:
        contact: str = bot_administrators.get('creator')
        text: str = 'Написать админ'

    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton(text=text, callback_data=sup_cb.new(telegram_id=contact)),
        InlineKeyboardButton(text='Отмена', callback_data='cancel')
    )
    return kb

