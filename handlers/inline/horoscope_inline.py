from aiogram.types import InlineQuery

from loader import dp
from utils.database_manage.sql.sql_commands import DB_USERS
from utils.keyboards.for_choosing_zodiac_kb import choice_zodiac_keyboard


@dp.inline_handler(text='')
async def check_query(query: InlineQuery):
	"""
	User verification.
	:param query: inline update
	:return: button (only in russian lang)
	"""
	if await DB_USERS.check_invalid_user(telegram_id=query.from_user.id):
		return await query.answer(
			results=[],
			switch_pm_text='Бот недоступен -> подключить бота',
			switch_pm_parameter='connect_user',
			cache_time=5,
			is_personal=True
		)


@dp.inline_handler(text='гороскоп')
async def get_inline_horoscope(query: InlineQuery):
	"""
	Shows the horoscope (only in russian lang).
	:param query: inline update
	"""
	lang: str = await DB_USERS.select_bot_language(query.from_user.id)
	await query.answer(
		results=await choice_zodiac_keyboard(lang=lang, inline=True),
		cache_time=60
	)

# Todo: переписать валидацию
