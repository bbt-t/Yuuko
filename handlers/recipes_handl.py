from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery, ChatActions, ContentType

from loader import dp
from middlewares.throttling import rate_limit
from utils.database_manage.sql.sql_commands import DB_USERS
from utils.keyboards.recipe_kb import pagination_recipe_keyboard


@rate_limit(2, key='recipe')
@dp.message_handler(Command('recipe'))
async def write_or_memorize_recipes(message: Message, state: FSMContext):
	lang, skin = await DB_USERS.select_lang_and_skin(telegram_id=message.from_user.id)

	await message.delete()
	msg_sticker = await message.answer_sticker(skin.welcome.value, disable_notification=True)
	await message.answer(
		'Чего изволите?' if lang == 'ru' else 'What do we do?',
		reply_markup=await pagination_recipe_keyboard(is_action=True))
	await state.set_state('recipe_name_entry')
	async with state.proxy() as data:
		data['lang'] = lang
		data['msg_sticker_id'] = msg_sticker.message_id


@dp.callback_query_handler(text={'receipt_of_prescription_info', 'recipe_name'}, state='recipe_name_entry')
async def write_recipe(call: CallbackQuery, state: FSMContext):
	async with state.proxy() as data:
		lang, msg_sticker_id = data.values()
		del data['msg_sticker_id']

	await dp.bot.delete_message(chat_id=call.message.chat.id, message_id=msg_sticker_id)
	msg_with_name: Message = await call.message.edit_text(
		'имя?',
		reply_markup=await pagination_recipe_keyboard()
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
			reply_markup=await pagination_recipe_keyboard()
		)
		await state.set_state('recipe_ingredients')
		async with state.proxy() as data:
			data['name_recipe'] = name
			data['msg_with_ingredients_id'] = msg_with_ingredients.message_id
	else:
		await message.reply('Слишком большое 🧐 название... попробуй ещё раз')
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
		reply_markup=await pagination_recipe_keyboard(),
	)
	await state.set_state('and_now_the_recipe')


@dp.message_handler(state='and_now_the_recipe')
async def write_and_now_recipe(message: Message, state: FSMContext):
	async with state.proxy() as data:
		lang, name_recipe, ingredients = data.values()
	try:
		await DB_USERS.add_recipe(
			telegram_id=message.from_user.id,
			name=name_recipe,
			ingredients=ingredients,
			recipe=message.text
		)
	except:
		await message.answer('Что-то пошло не так 😔')
	else:
		await message.answer('ГОТОВО! 🥳')
	finally:
		await state.finish()


@dp.message_handler(state='get_the_recipe')
async def memorize_recipes(message: Message, state: FSMContext):
	async with state.proxy() as data:
		lang = data['lang']

	await message.answer_chat_action(ChatActions.TYPING)
	try:
		match await DB_USERS.select_recipe(telegram_id=message.from_user.id, name=message.text):
			case ingredients, recipe, photo_url:
				await message.answer_photo(photo_url)
			case ingredients, recipe:
				await message.answer('ВОТ:\n')
				await message.answer('Если захочешь добавить фото, вызови меня ещё раз :)')
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


@dp.callback_query_handler(text='receipt_add_photo', state='recipe_name_entry')
async def recipe_send_photo(call: CallbackQuery, state: FSMContext):
	async with state.proxy() as data:
		lang, msg_sticker_id = data.values()
		del data['msg_sticker_id']

	await call.message.delete()
	await dp.bot.delete_message(chat_id=call.message.chat.id, message_id=msg_sticker_id)
	await call.answer('Жду фотку...', show_alert=True)
	await call.message.answer('Для моего удобства, плз, напиши имя рецепта в комментарии с фото :)')
	await state.set_state('recipe_photo_reception')


@dp.message_handler(state='recipe_photo_reception', content_types=ContentType.TEXT)
async def recipe_photo_reception_name(message: Message, state: FSMContext):
	name: str = message.text
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


@dp.message_handler(state='recipe_photo_reception', content_types=ContentType.PHOTO)
async def recipe_photo_reception(message: Message, state: FSMContext):
	photo_url: str = message.photo[-1].file_id
	async with state.proxy() as data:
		try:
			name: str = data['name']
		except KeyError:
			name: str = message.caption

	if name:
		await DB_USERS.update_recipe_photo(telegram_id=message.from_user.id, name=name, photo_url=photo_url)
		await message.answer('Фото добавлено! 🥳')
		await state.finish()
	else:
		async with state.proxy() as data:
			data['photo_url'] = photo_url

		return await message.answer('Имя рецепта?\n(ну, куда добавляем фотку...)')
	await state.finish()

# ToDo: Добавить проверку на существование имени рецепта в базе при добавлении фото.
# ToDo: Реализовать соответствующий ответ/ы.
# ToDo: Проверить на правильность логики/ошибки при обращении к несуществующему имени.

# ToDo: Реализовать доп.кнопку при записи рецепта для добавления фото.
# ToDo: Реализовать показ всех сохранённых имён рецептов (если есть фото, то показывать).

