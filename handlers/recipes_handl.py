from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery

from loader import dp
from middlewares.throttling import rate_limit
from utils.database_manage.sql.sql_commands import select_lang_and_skin, add_recipe, select_recipe
from utils.keyboards.recipe_kb import pagination_recipe_keyboard


@rate_limit(2, key='recipe')
@dp.message_handler(Command('recipe'))
async def write_or_memorize_recipes(message: Message, state: FSMContext):
	lang, skin = await select_lang_and_skin(telegram_id=message.from_user.id)

	await message.delete()
	#await message.answer_sticker(СТИКЕР)
	await message.answer('Чего изволите?', reply_markup=await pagination_recipe_keyboard())
	await state.set_state('recipe_name_entry')
	async with state.proxy() as data:
		data['lang'] = lang


@dp.callback_query_handler(text={'receipt_of_prescription_info', 'recipe_name'}, state='recipe_name_entry')
async def write_recipe(call: CallbackQuery, state: FSMContext):
	async with state.proxy() as data:
		lang: str = data['lang']

	await call.message.delete()
	msg_with_name: Message = await call.message.answer(
		'имя?',
		reply_markup=await pagination_recipe_keyboard(action='with_cancel')
	)
	if call.data == 'receipt_of_prescription_info':
		async with state.proxy() as data:
			data['msg_with_name'] = msg_with_name.message_id
	elif call.data == 'recipe_name':
		await state.set_state('get_the_recipe')


@dp.message_handler(state='recipe_name_entry')
async def write_recipe_name(message: Message, state: FSMContext):
	async with state.proxy() as data:
		lang, for_del_msg = data.get('lang'), data.get('msg_with_name')
		del data['msg_with_name']

	if len(name := message.text) <= 32:
		await message.delete()
		await dp.bot.delete_message(chat_id=message.chat.id, message_id=for_del_msg)
		msg_with_ingredients: Message = await message.answer(
			'ингредиенты?\n\n(списком или каждый ингредиент в новой строке)',
			reply_markup=await pagination_recipe_keyboard(action='with_cancel')
		)
		await state.set_state('recipe_ingredients')
		async with state.proxy() as data:
			data['name_recipe'] = name
			data['msg_with_ingredients_id'] = msg_with_ingredients.message_id
	else:
		await message.reply('Слишком большое название... попробуй ещё раз')
		await state.finish()


@dp.message_handler(state='recipe_ingredients')
async def write_recipe_ingredients(message: Message, state: FSMContext):
	async with state.proxy() as data:
		lang, for_del_msg = data.get('lang'), data.get('msg_with_ingredients_id')
		data['ingredients'] = message.text
		del data['msg_with_ingredients_id']

	await message.delete()
	await dp.bot.delete_message(chat_id=message.chat.id, message_id=for_del_msg)
	await message.answer(
		'а теперь сам рецепт',
		reply_markup=await pagination_recipe_keyboard(action='with_cancel'),
	)
	await state.set_state('and_now_the_recipe')


@dp.message_handler(state='and_now_the_recipe')
async def write_and_now_recipe(message: Message, state: FSMContext):
	async with state.proxy() as data:
		lang: str = data.get('lang')
		name_recipe: str = data.get('name_recipe')
		ingredients: str = data.get('ingredients')

	await message.delete()
	try:
		await add_recipe(
			telegram_id=message.from_user.id,
			name=name_recipe,
			ingredients=ingredients,
			recipe=message.text
		)
	except:
		await message.answer('Что-то пошло не так :(')
	else:
		await message.answer('ГОТОВО!')
	finally:
		await state.finish()


@dp.message_handler(state='get_the_recipe')
async def memorize_recipes(message: Message, state: FSMContext):
	async with state.proxy() as data:
		lang = data['lang']

	try:
		ingredients, recipe = await select_recipe(telegram_id=message.from_user.id, name=message.text)
	except TypeError:
		await message.reply('Нет такого :(')
	else:
		await message.answer(
			f'Сделано!\n\n'
			f'<b>Ингридиенты:</b>\n{ingredients}\n\n'
			f'<b>Рецепт:</b>\n{recipe}')
	finally:
		await state.finish()
