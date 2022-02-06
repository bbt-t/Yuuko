from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


tools_choice_kb = InlineKeyboardMarkup()
tools_choice_kb.add(
    InlineKeyboardButton(text='сбросить кодовое слово', callback_data='reset_user_codeword'),
    InlineKeyboardButton(text='отмена', callback_data='cancel')
)
