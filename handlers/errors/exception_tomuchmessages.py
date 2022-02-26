from time import sleep

from aiogram.types import Update
from aiogram.utils.exceptions import ToMuchMessages

from loader import dp, logger_guru


@dp.errors_handler(exception=ToMuchMessages)
async def error_bot_blocked(update: Update, exception: ToMuchMessages) -> bool:
	"""
	If the limit API for sending messages is exceeded.
	"""
	logger_guru.critical(f"Can'not send message!\n{update=}\n{exception=}")
	sleep(1)
	await dp.bot.send_message(chat_id=update.message.chat.id, text=update.message.text)
	return True
