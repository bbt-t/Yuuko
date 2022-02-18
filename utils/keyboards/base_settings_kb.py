from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


settings_keyboard_ru = InlineKeyboardMarkup(row_width=3)
settings_keyboard_ru.add(
	InlineKeyboardButton(text='Оповещение о погоде', callback_data='set_weather'),
	InlineKeyboardButton(text="Время Todo'ек", callback_data='set_time_todo'),
	InlineKeyboardButton(text='Сменить стикерпак', callback_data='set_skin'),
	InlineKeyboardButton(text='отмена', callback_data='cancel')
)

settings_keyboard_en = InlineKeyboardMarkup(row_width=3)
settings_keyboard_en.add(
	InlineKeyboardButton(text='Weather alert', callback_data='set_weather'),
	InlineKeyboardButton(text='Todo time', callback_data='set_time_todo'),
	InlineKeyboardButton(text='Change sticker pack', callback_data='set_skin'),
	InlineKeyboardButton(text='Cancel', callback_data='cancel')
)
