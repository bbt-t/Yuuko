from aiogram.utils.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import AdminsBot




sup_cb = CallbackData('sup_ask', 'telegram_id')


async def sup_kb(telegram_id=None):
    match telegram_id:
        case int(telegram_id):
            contact = telegram_id
            text = 'Ответить пользователю'
        case _:
            contact = AdminsBot.creator.value
            text = 'Написать админу'

    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton(text=text, callback_data=sup_cb.new(telegram_id=contact)),
        InlineKeyboardButton(text='Отмена', callback_data='cancel')
    )
    return kb

