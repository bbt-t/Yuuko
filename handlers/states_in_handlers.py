from aiogram.dispatcher.filters.state import StatesGroup, State


class TodoStates(StatesGroup):
	"""
	For todo_handl
	"""
	todo = State()
	reception_todo = State()


class PasswordStates(StatesGroup):
	"""
	For storing_passwords_handl
	"""
	check_personal_code = State()
	successful_auth_for_pass = State()
	set_name_pass = State()


class UserSettingStates(StatesGroup):
	"""
	For:
		user_settings
		day_todo_notification
		weather_status_handl
		changing_stikerpack_handl
		start_handl
	"""
	settings = State()
	time_todo = State()
	weather_on = State()


class RecipeStates(StatesGroup):
	"""
	For recipes_handl.
	"""
	recipe_manipulation = State()
	get_the_recipe = State()
	recipe_ingredients = State()
	and_now_the_recipe = State()
	recipe_photo_reception = State()

