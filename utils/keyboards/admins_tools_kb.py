from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


tools_choice_kb = InlineKeyboardMarkup(row_width=2)
tools_choice_kb.add(
    InlineKeyboardButton(text='сбросить кодовое слово', callback_data='reset_user_codeword'),
    InlineKeyboardButton(text='рассылка пользователям', callback_data='make_newsletter'),
    InlineKeyboardButton(text='отмена', callback_data='cancel')
)
