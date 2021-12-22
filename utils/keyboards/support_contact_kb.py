from aiogram.utils.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import admins_bot




sup_cb = CallbackData('sup_ask', 'telegram_id')


async def sup_kb(telegram_id=None):
    """
    Keyboard for feedback with the administration.
    :param telegram_id: user id
    :return: shaped inline-keyboard
    """
    match telegram_id:
        case int(telegram_id):
            contact = telegram_id
            text: str = 'Ответить пользователю'
        case _:
            contact: int = admins_bot.get('creator')
            text: str = 'Написать админу'

    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton(text=text, callback_data=sup_cb.new(telegram_id=contact)),
        InlineKeyboardButton(text='Отмена', callback_data='cancel')
    )
    return kb

