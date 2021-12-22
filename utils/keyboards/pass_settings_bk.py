from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


pass_choice_kb = InlineKeyboardMarkup()
item_1 = InlineKeyboardButton(text='Задать новый', callback_data='new_pass')
item_2 = InlineKeyboardButton(text='узнать уже сохранённый', callback_data='receive_pass')

pass_choice_kb.insert(item_1)
pass_choice_kb.insert(item_2)