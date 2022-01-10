from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.utils.exceptions import MessageNotModified

from loader import dp
from middlewares.throttling import rate_limit
from utils.horoscope.getting_horoscope import get_user_horoscope
from utils.keyboards.for_choosing_zodiac_kb import choice_zodiac_keyboard, choice_day_zodiac_keyboard




@rate_limit(5, key='horoscope')
@dp.message_handler(Command('horoscope'))
async def start_working_with_bot(message: Message, state: FSMContext):
    await message.answer('Заглянем в бууудууущее))...\n\n'
                         'так, СТОП! мне же нужна инфа о тебе,\n'
                         'говори свой знак зодиака!', reply_markup=choice_zodiac_keyboard)
    await message.delete()
    await state.set_state('waiting_for_zodiac_sign')


@dp.callback_query_handler(state='waiting_for_zodiac_sign')
async def get_horoscope(call: CallbackQuery, state: FSMContext):
    try:
        await call.message.edit_reply_markup(choice_day_zodiac_keyboard)
        async with state.proxy() as data:
            data['zodiac'] = call.data
    except MessageNotModified:
        async with state.proxy() as data:
            zodiac: str = data['zodiac']
        text_msg: str = await get_user_horoscope(zodiac=zodiac, when=call.data)

        await call.message.delete_reply_markup()
        await call.message.edit_text(text_msg)
        await state.finish()
