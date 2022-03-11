from aiogram.dispatcher.filters import Command
from aiogram.types import Message

from config import time_zone
from loader import dp, logger_guru
from middlewares.throttling import rate_limit
from utils.database_manage.sql.sql_commands import DB_USERS
from utils.lunar_haircut import lunar_calendar_haircut
from utils.misc.other_funcs import get_time_now


@rate_limit(2, key='hair')
@dp.message_handler(Command('hair'))
async def show_days_for_haircuts(message: Message):
    lang, skin = await DB_USERS.select_lang_and_skin(telegram_id=message.from_user.id)
    try:
        received_days: str = await lunar_calendar_haircut()
    except:
        logger_guru.exception('Haircuts Error')
        await message.reply_sticker(skin.something_is_wrong.value, disable_notification=True)
        await message.answer(
            'Что-то пошло не так...попробуй позже.' if lang == 'ru' else
            'Something went wrong... please try again later.'
        )
    else:
        if get_time_now(time_zone).day <= max(map(int, received_days.split(','))):
            if lang == 'ru':
                text_msg = (f'Привет!\nВот благоприятные дни для стрижки на текущий месяц:'
                            f'\n\n<code>{received_days}</code>')
            else:
                text_msg = (f'Hello!\nHere are auspicious days for a haircut for the current month:'
                            f'\n\n<code>{received_days}</code>')
            await message.answer(text_msg)
        else:
            await message.answer('На текущий месяц уже ничего нет.')
    finally:
        await message.delete()
