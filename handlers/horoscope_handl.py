from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.utils.exceptions import MessageNotModified

from loader import dp
from middlewares.throttling import rate_limit
from utils.database_manage.sql.sql_commands import select_bot_language
from utils.getting_horoscope import get_user_horoscope_ru, get_user_horoscope_en
from utils.keyboards.for_choosing_zodiac_kb import (choice_zodiac_keyboard_ru, choice_day_zodiac_keyboard_ru,
                                                    choice_zodiac_keyboard_en, choice_day_zodiac_keyboard_en)


@rate_limit(5, key='horoscope')
@dp.message_handler(Command('horoscope'))
async def start_working_with_bot(message: Message, state: FSMContext):
    match lang := await select_bot_language(telegram_id=message.from_user.id):
        case 'ru':
            await message.answer(
                'Заглянем в бууудууущее 🙈\n\n'
                'так, СТОП! мне же нужна инфа о тебе,\n'
                'говори свой знак зодиака!', reply_markup=choice_zodiac_keyboard_ru
            )
        case _:
            await message.answer(
                "Let's look into the future 🙈\n\n"
                "hmm, STOP! I need info about you,\n"
                "tell me your zodiac sign!", reply_markup=choice_zodiac_keyboard_en
            )

    await message.delete()
    await state.set_state('waiting_for_zodiac_sign')
    async with state.proxy() as data:
        data['lang'] = lang


@dp.callback_query_handler(state='waiting_for_zodiac_sign')
async def get_horoscope(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        lang: str = data['lang']

    try:
        if lang == 'ru':
            await call.message.edit_reply_markup(choice_day_zodiac_keyboard_ru)
        else:
            await call.message.edit_reply_markup(choice_day_zodiac_keyboard_en)
        async with state.proxy() as data:
            data['zodiac'] = call.data
    except MessageNotModified:
        async with state.proxy() as data:
            zodiac: str = data['zodiac']
        if lang == 'ru':
            text_msg: str = await get_user_horoscope_ru(zodiac=zodiac, when=call.data)
        else:
            text_msg: str = await get_user_horoscope_en(zodiac=zodiac, when=call.data)

        await call.message.delete_reply_markup()
        await call.message.edit_text(text_msg)
        await state.finish()
