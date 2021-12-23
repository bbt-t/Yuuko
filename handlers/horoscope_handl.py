from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message

from loader import dp
from middlewares.throttling import rate_limit
from utils.horoscope.getting_horoscope import get_user_horoscope




@rate_limit(5, key='horoscope')
@dp.message_handler(Command('horoscope'))
async def start_working_with_bot(message: Message, state: FSMContext):
    await message.answer('Заглянем в бууудууущее))...\n\n'
                         'так, СТОП! мне же нужна инфа о тебе,\n'
                         'говори свой знак зодиака!')

    await state.set_state('waiting_for_zodiac_sign')


@dp.message_handler(state='waiting_for_zodiac_sign')
async def get_horoscope(message: Message, state: FSMContext):
    zodiac: str = message.text.replace(' ', '')
    try:
        text_msg: str = await get_user_horoscope(zodiac=zodiac)
        await message.answer(text_msg)
    except KeyError:
        await message.reply('Что-то не понятное написано, попробуй ещё раз.')
    else:
        await state.finish()
