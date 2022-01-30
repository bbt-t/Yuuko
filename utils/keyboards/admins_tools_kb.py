from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


tools_choice_kb = InlineKeyboardMarkup()

item_1 = InlineKeyboardButton(text='сбросить кодовое слово', callback_data='reset_user_codeword')
item_2 = InlineKeyboardButton(text='отмена', callback_data='cancel')

tools_choice_kb.insert(item_1)
tools_choice_kb.insert(item_2)
