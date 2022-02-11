from aiogram.dispatcher.filters import Command
from aiogram.types import Message

from loader import dp
from middlewares.throttling import rate_limit
from utils.database_manage.sql.sql_commands import select_bot_language
from utils.keyboards.start_handl_choice_kb import choice_of_assistant_kb_ru, choice_of_assistant_kb_en


@rate_limit(5, key='change_skin')
@dp.message_handler(Command('change_skin'))
async def start_working_with_bot(message: Message):
    match await select_bot_language(telegram_id=message.from_user.id):
        case 'ru':
            await message.answer("На какой меняем?", reply_markup=choice_of_assistant_kb_ru)
        case _:
            await message.answer("What are we changing to?", reply_markup=choice_of_assistant_kb_en)
