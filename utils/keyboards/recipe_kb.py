from aiogram.types.inline_keyboard import InlineKeyboardMarkup, InlineKeyboardButton


async def pagination_recipe_keyboard(is_action: bool = None) -> InlineKeyboardMarkup:
	action_choice_recipe_keyboard = InlineKeyboardMarkup(row_width=1)
	action_choice_recipe_keyboard.add(
		InlineKeyboardButton(text='отмена', callback_data='cancel')
	)
	if is_action:
		action_choice_recipe_keyboard.add(
			InlineKeyboardButton(text='Вспомнить', callback_data='recipe_name'),
			InlineKeyboardButton(text='Записать', callback_data='receipt_of_prescription_info'),
			InlineKeyboardButton(text='Добивать фото', callback_data='receipt_add_photo'),
		)
	return action_choice_recipe_keyboard

