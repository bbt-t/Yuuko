from typing import Final, Optional

from aiogram.utils.callback_data import CallbackData
from aiogram.types.inline_keyboard import InlineKeyboardMarkup, InlineKeyboardButton


pag_cb = CallbackData("paginator", "key", "page")


async def recipe_keyboard(is_first: Optional[bool] = None) -> InlineKeyboardMarkup:
	"""
	Keyboard to select action.
	:param is_first: keyboard call for initial handler
	:return: keyboard
	"""
	action_choice_recipe_keyboard = InlineKeyboardMarkup(row_width=2)
	if is_first:
		action_choice_recipe_keyboard.add(
			InlineKeyboardButton(text='Вспомнить', callback_data='recipe_name'),
			InlineKeyboardButton(text='Показать все', callback_data='get_all_recipes'),
			InlineKeyboardButton(text='Записать', callback_data='receipt_of_prescription_info'),
			InlineKeyboardButton(text='Добивать фото', callback_data='receipt_add_photo'),
		)
		action_choice_recipe_keyboard.row()
	action_choice_recipe_keyboard.add(
		InlineKeyboardButton(text='отмена', callback_data='cancel')
	)
	return action_choice_recipe_keyboard


def pagination_recipe_keyboard(max_pages: int, key: str = 'recipe', page: int = 0) -> InlineKeyboardMarkup:
	"""
	Keyboard for pagination according to saved user recipes.
	:param max_pages: total number of recipes
	:param key: identifier
	:param page: "page" number
	:return: keyboard
	"""
	translate_number: Final[dict] = {
		'0': "0️⃣",
		'1': "1️⃣",
		'2': "2️⃣",
		'3': "3️⃣",
		'4': "4️⃣",
		'5': "5️⃣",
		'6': "6️⃣",
		'7': "7️⃣",
		'8': "8️⃣",
		'9': "9️⃣",
	}
	show_page: str = str(page + 1).translate(str.maketrans(translate_number))

	pre_page, next_page = page - 1, page + 1
	pre_page_text, current_page_text, next_page_text = "⏪  ", f">> {show_page} <<", "  ⏩"

	keyboard = InlineKeyboardMarkup()
	if pre_page >= 0:
		keyboard.insert(
			InlineKeyboardButton(
				text=pre_page_text,
				callback_data=pag_cb.new(key=key, page=pre_page)
			)
		)
	keyboard.insert(
		InlineKeyboardButton(
			text=current_page_text,
			callback_data=pag_cb.new(key=key, page="current_page")
		)
	)
	if next_page < max_pages:
		keyboard.insert(
			InlineKeyboardButton(
				text=next_page_text,
				callback_data=pag_cb.new(key=key, page=next_page)
			)
		)
	keyboard.add(InlineKeyboardButton(text='отмена', callback_data='cancel'))
	return keyboard
