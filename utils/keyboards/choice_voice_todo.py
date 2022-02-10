from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


choice_voice_todo_keyboard = InlineKeyboardMarkup()
choice_voice_todo_keyboard.add(
    InlineKeyboardButton(text='конечно', callback_data='choice_voice_yep'),
	InlineKeyboardButton(text='нет, спасибо', callback_data='choice_voice_no')
)
