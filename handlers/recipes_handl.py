from typing import Optional

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery, ChatActions, ContentType

from sqlalchemy.exc import SQLAlchemyError

from handlers.states_in_handlers import RecipeStates
from loader import dp
from middlewares.throttling import rate_limit
from utils.database_manage.sql.sql_commands import DB_USERS
from utils.keyboards.recipe_kb import recipe_keyboard, pagination_recipe_keyboard, pag_cb


@rate_limit(2, key='recipe')
@dp.message_handler(Command('recipe'))
async def write_or_memorize_recipes(message: Message, state: FSMContext) -> None:
	lang, skin = await DB_USERS.select_lang_and_skin(telegram_id=message.from_user.id)

	await message.delete()
	msg_sticker: Message = await message.answer_sticker(skin.welcome.value, disable_notification=True)
	await message.answer(
		'Чего изволите?' if lang == 'ru' else 'What do we do?',
		reply_markup=await recipe_keyboard(is_first=True))

	await RecipeStates.first()
	async with state.proxy() as data:
		data['lang'], data['msg_sticker_id'] = lang, msg_sticker.message_id


@dp.callback_query_handler(
	text={'receipt_of_prescription_info', 'recipe_name'},
	state=RecipeStates.recipe_manipulation
)
async def write_recipe(call: CallbackQuery, state: FSMContext) -> None:
	async with state.proxy() as data:
		lang: str = data.get('lang')
		await dp.bot.delete_message(
			chat_id=call.message.chat.id,
			message_id=data.pop('msg_sticker_id')
		)

	msg_with_name: Message = await call.message.edit_text(
		'имя?',
		reply_markup=await recipe_keyboard()
	)
	if call.data == 'receipt_of_prescription_info':
		async with state.proxy() as data:
			data['msg_with_name'] = msg_with_name.message_id
	elif call.data == 'recipe_name':
		await RecipeStates.next()


@dp.message_handler(state=RecipeStates.recipe_manipulation)
async def write_recipe_name(message: Message, state: FSMContext) -> Optional[Message]:
	name: str = message.text

	if await DB_USERS.check_recipe_name(telegram_id=message.from_user.id, name=name):
		await state.finish()
		return await message.reply('Рецепт с таким именем уже существует!')

	async with state.proxy() as data:
		lang, for_del_msg = data.get('lang'), data.pop('msg_with_name')

	if len(name) <= 64:
		await dp.bot.delete_message(chat_id=message.chat.id, message_id=for_del_msg)
		msg_with_ingredients: Message = await message.answer(
			'ингредиенты?\n\n(списком или каждый ингредиент в новой строке)',
			reply_markup=await recipe_keyboard()
		)
		await RecipeStates.recipe_ingredients.set()
		async with state.proxy() as data:
			data['name_recipe'] = name
			data['msg_with_ingredients_id'] = msg_with_ingredients.message_id
	else:
		await message.reply('Слишком большое 🧐 название... попробуй ещё раз')
		await state.finish()


@dp.message_handler(state=RecipeStates.recipe_ingredients)
async def write_recipe_ingredients(message: Message, state: FSMContext) -> None:
	async with state.proxy() as data:
		lang, for_del_msg = data.get('lang'), data.pop('msg_with_ingredients_id')
		data['ingredients'] = message.text

	await message.delete()
	await dp.bot.delete_message(chat_id=message.chat.id, message_id=for_del_msg)
	await message.answer(
		'а теперь сам рецепт',
		reply_markup=await recipe_keyboard(),
	)
	await RecipeStates.next()


@dp.message_handler(state=RecipeStates.and_now_the_recipe)
async def write_and_now_recipe(message: Message, state: FSMContext) -> None:
	async with state.proxy() as data:
		lang, name_recipe, ingredients = data.values()
	try:
		await DB_USERS.add_recipe(
			telegram_id=message.from_user.id,
			name=name_recipe,
			ingredients=ingredients,
			recipe=message.text
		)
	except SQLAlchemyError:
		await message.answer('Что-то пошло не так 😔')
	else:
		await message.answer('ГОТОВО! 🥳')
	finally:
		await state.finish()


@dp.message_handler(state=RecipeStates.get_the_recipe)
async def memorize_recipes(message: Message, state: FSMContext) -> None:
	async with state.proxy() as data:
		lang: str = data.get('lang')

	await message.answer_chat_action(ChatActions.TYPING)
	try:
		ingredients, recipe, photo_url = await DB_USERS.select_recipe(
			telegram_id=message.from_user.id, name=message.text
		)
		if not photo_url:
			await message.answer(
				'Если захочешь добавить фото, вызови меня ещё раз :)'
			)
		else:
			await message.answer_photo(photo_url)
	except TypeError:
		await message.reply(
			'Нет такого :(' if lang == 'ru' else 'There is no such :('
		)
	else:
		await message.answer(
			f'<b>Ингридиенты:</b>\n{ingredients}\n\n'
			f'<b>Рецепт:</b>\n{recipe}')
	finally:
		await state.finish()


@dp.callback_query_handler(text='receipt_add_photo', state=RecipeStates.recipe_manipulation)
async def recipe_send_photo(call: CallbackQuery, state: FSMContext) -> None:
	async with state.proxy() as data:
		lang, msg_sticker_id = data.values()
		del data['msg_sticker_id']

	await call.message.delete()
	await dp.bot.delete_message(chat_id=call.message.chat.id, message_id=msg_sticker_id)
	await call.answer('Жду фотку...', show_alert=True)
	await call.message.answer('Для моего удобства, плз, напиши имя рецепта в комментарии с фото :)')

	await RecipeStates.last()


@dp.message_handler(state=RecipeStates.recipe_photo_reception, content_types=ContentType.TEXT)
async def recipe_photo_reception_name(message: Message, state: FSMContext) -> Optional[Message]:
	name: str = message.text

	if not await DB_USERS.check_recipe_name(telegram_id=message.from_user.id, name=name):
		await state.finish()
		return await message.reply('Нет такого рецепта :(')

	async with state.proxy() as data:
		try:
			photo_url: str = data['photo_url']
			await DB_USERS.update_recipe_photo(
				telegram_id=message.from_user.id, name=name, photo_url=photo_url
			)
			await message.answer('Фото добавлено! 🥳')
			await state.finish()
		except KeyError:
			data['name'] = name
			return await message.answer('Фотку! фотку присылай!')


@dp.message_handler(state=RecipeStates.recipe_photo_reception, content_types=ContentType.PHOTO)
async def recipe_photo_reception(message: Message, state: FSMContext) -> Optional[Message]:
	photo_url: str = message.photo[-1].file_id
	async with state.proxy() as data:
		try:
			name: str = data['name']
		except KeyError:
			name: str = message.caption
			if not await DB_USERS.check_recipe_name(telegram_id=message.from_user.id, name=name):
				await state.finish()
				return await message.reply('Нет такого рецепта :(')
	if name:
		await DB_USERS.update_recipe_photo(telegram_id=message.from_user.id, name=name, photo_url=photo_url)
		await message.answer('Фото добавлено! 🥳')
		await state.finish()
	else:
		async with state.proxy() as data:
			data['photo_url'] = photo_url

		return await message.answer('Имя рецепта?\n(ну, куда добавляем фотку...)')
	await state.finish()


@dp.callback_query_handler(text='get_all_recipes', state=RecipeStates.recipe_manipulation)
async def show_all_recipes(call: CallbackQuery, state: FSMContext) -> CallbackQuery | None:
	all_recipes: list = await DB_USERS.select_all_recipes(telegram_id=call.from_user.id)
	try:
		first_recipe_info: dict = all_recipes[0]
	except IndexError:
		skin = await DB_USERS.select_skin(telegram_id=call.from_user.id)
		await call.message.answer_sticker(skin.something_is_wrong.value, disable_notification=True)
		return await call.answer('Нетю ни одного рецепта :(', show_alert=True)
	max_pages: int = len(all_recipes)
	text_msg: str = (
		f'<b>Ингридиенты:</b>\n{first_recipe_info.get("ingredients")}\n\n'
		f'<b>Рецепт:</b>\n{first_recipe_info.get("recipe")}'
	)
	async with state.proxy() as data:
		lang, msg_sticker_id = data.get('lang'), data.pop('msg_sticker_id')
		data['all_recipes'], data['max_pages'] = all_recipes, max_pages

	await call.message.delete()
	await dp.bot.delete_message(chat_id=call.message.chat.id, message_id=msg_sticker_id)

	if first_recipe_info.get('photo_id'):
		msg_with_photo: Message = await call.message.answer_photo(first_recipe_info.get('photo_id'))
		async with state.proxy() as data:
			data['msg_with_photo_id'] = msg_with_photo.message_id

	if max_pages > 1:
		await call.message.answer(
			text_msg, reply_markup=pagination_recipe_keyboard(max_pages=max_pages)
		)
	elif max_pages == 1:
		await call.message.edit_text(text_msg)
		await state.finish()


@dp.callback_query_handler(pag_cb.filter(page="current_page"), state=RecipeStates.recipe_manipulation)
async def recipe_skip_current_page(call: CallbackQuery) -> None:
	await call.answer(cache_time=60)


@dp.callback_query_handler(pag_cb.filter(key='recipe'), state=RecipeStates.recipe_manipulation)
async def recipes_pag_chosen_page(call: CallbackQuery, state: FSMContext, callback_data: dict) -> None:
	async with state.proxy() as data:
		if data.get('msg_with_photo_id'):
			await dp.bot.delete_message(
				chat_id=call.message.chat.id,
				message_id=data.pop('msg_with_photo_id')
			)
		lang, all_recipes, max_pages = data.values()

	current_page: int = int(callback_data.get('page'))
	recipe_info: dict = all_recipes[current_page]

	if recipe_info.get('photo_id'):
		msg_with_photo: Message = await call.message.answer_photo(recipe_info.get('photo_id'))
		async with state.proxy() as data:
			data['msg_with_photo_id'] = msg_with_photo.message_id

	await call.message.delete()
	await call.message.answer(
		f'<b>Ингридиенты:</b>\n{recipe_info.get("ingredients")}\n\n'
		f'<b>Рецепт:</b>\n{recipe_info.get("recipe")}',
		reply_markup=pagination_recipe_keyboard(max_pages=max_pages, page=current_page)
	)
