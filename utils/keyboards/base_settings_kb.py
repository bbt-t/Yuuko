from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


settings_keyboard_ru = InlineKeyboardMarkup(row_width=3)
settings_keyboard_ru.add(
	InlineKeyboardButton(text='Погода', callback_data='set_weather'),
	InlineKeyboardButton(text="Todo'шки", callback_data='set_time_todo'),
	InlineKeyboardButton(text='Стикерпак', callback_data='set_skin'),
	InlineKeyboardButton(text='отмена', callback_data='cancel')
)

settings_keyboard_en = InlineKeyboardMarkup(row_width=3)
settings_keyboard_en.add(
	InlineKeyboardButton(text='Weather', callback_data='set_weather'),
	InlineKeyboardButton(text='Todo', callback_data='set_time_todo'),
	InlineKeyboardButton(text='Sticker pack', callback_data='set_skin'),
	InlineKeyboardButton(text='Cancel', callback_data='cancel')
)
