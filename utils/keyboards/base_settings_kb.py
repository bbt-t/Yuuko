from typing import Literal

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from utils.misc.other_funcs import create_keyboard_button


def settings_keyboard(lang: Literal['ru', 'en'] = 'ru') -> InlineKeyboardMarkup:
	"""

	:param lang:
	:return:
	"""
	callback_data: tuple = 'set_weather', 'set_time_todo', 'set_skin', 'cancel'
	text_ru: tuple = 'Погода', "Todo'шки", 'Стикерпак', 'отмена'
	text_en: tuple = 'Weather', 'Todo', 'Sticker pack', 'Cancel'

	return create_keyboard_button(
		text=text_ru if lang == 'ru' else text_en,
		callback_data=callback_data,
	)


def choice_settings(
		lang: Literal['ru', 'en'] = 'ru',
		is_todo: bool = False,
		is_weather: bool = False
) -> InlineKeyboardMarkup:
	"""

	:param lang:
	:param is_todo:
	:param is_weather:
	:return:
	"""
	text_ru: tuple = 'вкл/изменить', 'выкл',
	text_en: tuple = 'on/edit', 'off',

	if is_weather:
		callback_data: tuple = 'weather_on_settings', 'weather_off_settings',
	if is_todo:
		callback_data: tuple = 'todo_on_settings', 'todo_off_settings',

	return create_keyboard_button(
		text=text_ru if lang == 'ru' else text_en,
		callback_data=callback_data,
	)

