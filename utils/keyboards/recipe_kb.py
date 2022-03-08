from aiogram.types.inline_keyboard import InlineKeyboardMarkup, InlineKeyboardButton


async def pagination_recipe_keyboard(action: str = None) -> InlineKeyboardMarkup:
	action_choice_recipe_keyboard = InlineKeyboardMarkup(row_width=2)
	if action == 'with_cancel':
		action_choice_recipe_keyboard.add(
			InlineKeyboardButton(text='отмена', callback_data='cancel')
		)
	elif action is None:
		action_choice_recipe_keyboard.add(
			InlineKeyboardButton(text='Вспомнить', callback_data='recipe_name'),
			InlineKeyboardButton(text='Записать', callback_data='receipt_of_prescription_info'),
			InlineKeyboardButton(text='отмена', callback_data='cancel')
		)
	return action_choice_recipe_keyboard

