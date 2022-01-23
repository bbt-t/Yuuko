from aiogram.dispatcher.filters import Command
from aiogram.types import Message

from loader import dp
from middlewares.throttling import rate_limit
from utils.lunar_haircut import lunar_calendar_haircut
from utils.misc.enums_data import SendStickers


@rate_limit(5, key='hair')
@dp.message_handler(Command('hair'))
async def show_days_for_haircuts(message: Message):
    if text_msg := await lunar_calendar_haircut():
        await message.answer(f'Привет!\nВот благоприятные дни для стрижки на текущий месяц:\n\n'
                             f'<code>{text_msg}</code>')
        await message.delete()
    else:
        await message.reply_sticker(SendStickers.something_is_wrong.value)
        await message.answer('Что-то пошло не так...попробуй позже.')
