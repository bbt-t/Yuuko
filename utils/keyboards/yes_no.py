from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


yes_no_choice_kb = InlineKeyboardMarkup()
yes_no_choice_kb.add(
	InlineKeyboardButton(text='давай включим и погоду!', callback_data='weather_add'),
	InlineKeyboardButton(text='не, пока не надо', callback_data='cancel')
)
