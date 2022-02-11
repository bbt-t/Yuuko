from aiogram.dispatcher.filters import Command
from aiogram.types import Message

from loader import dp
from middlewares.throttling import rate_limit
from utils.database_manage.sql.sql_commands import select_lang_and_skin
from utils.lunar_haircut import lunar_calendar_haircut


@rate_limit(5, key='hair')
@dp.message_handler(Command('hair'))
async def show_days_for_haircuts(message: Message):
    lang, skin = await select_lang_and_skin(telegram_id=message.from_user.id)

    if text_msg := await lunar_calendar_haircut():
        if lang == 'ru':
            text_msg = (f'Привет!\nВот благоприятные дни для стрижки на текущий месяц:'
                        f'\n\n<code>{text_msg}</code>')
        else:
            text_msg = (f'Hello!\nHere are auspicious days for a haircut for the current month:'
                        f'\n\n<code>{text_msg}</code>')
        await message.delete()
        await message.answer(text_msg)
    else:
        await message.reply_sticker(skin.something_is_wrong.value)
        await message.answer('Что-то пошло не так...попробуй позже.')
