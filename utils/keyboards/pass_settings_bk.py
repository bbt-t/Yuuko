from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


pass_choice_kb = InlineKeyboardMarkup()
pass_choice_kb.add(
	InlineKeyboardButton(text='Задать новый', callback_data='new_pass'),
	InlineKeyboardButton(text='узнать уже сохранённый', callback_data='receive_pass')
)
