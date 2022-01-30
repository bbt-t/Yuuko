from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


choice_voice_todo_keyboard = InlineKeyboardMarkup()

item_1 = InlineKeyboardButton(text='конечно', callback_data='choice_voice_yep')
item_2 = InlineKeyboardButton(text='нет, спасибо', callback_data='choice_voice_no')

choice_voice_todo_keyboard.insert(item_1)
choice_voice_todo_keyboard.insert(item_2)