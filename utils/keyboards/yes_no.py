from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


yes_no_choice_kb = InlineKeyboardMarkup()
item_1 = InlineKeyboardButton(text='давай включим и погоду!', callback_data='weather_add')
item_2 = InlineKeyboardButton(text='не, пока не надо', callback_data='cancel')

yes_no_choice_kb.insert(item_1)
yes_no_choice_kb.insert(item_2)