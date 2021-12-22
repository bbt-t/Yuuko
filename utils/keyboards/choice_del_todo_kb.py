from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


choice_del_todo_keyboard = InlineKeyboardMarkup()
item_1 = InlineKeyboardButton(text='отметить выполненые', callback_data='choice_del_todo')
item_2 = InlineKeyboardButton(text='всё сделано!', callback_data='delete_all_todo')

choice_del_todo_keyboard.insert(item_1)
choice_del_todo_keyboard.insert(item_2)
