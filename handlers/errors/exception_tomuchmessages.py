from aiogram.types import Update
from aiogram.utils.exceptions import ToMuchMessages

from loader import dp, logger_guru
from config import bot_administrators


@dp.errors_handler(exception=ToMuchMessages)
async def error_bot_blocked(update: Update, exception: ToMuchMessages) -> bool:
	"""
	If the limit API for sending messages is exceeded.
	"""
	logger_guru.critical(f"Can'not send message!\n{update=}\n{exception=}")
	await dp.bot.send_message(
		chat_id=bot_administrators.get('creator'),
		text=f"Can'not send message!\n{update=}\n{exception=}"
	)
	return True
