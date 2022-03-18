from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from handlers.states_in_handlers import UserSettingStates
from loader import dp
from utils.keyboards.start_handl_choice_kb import get_start_keyboard


@dp.callback_query_handler(text='set_skin', state=UserSettingStates.settings)
async def choose_a_sticker_pack(call: CallbackQuery, state: FSMContext) -> None:
    async with state.proxy() as data:
        if data.get('lang') == 'ru':
            await call.message.answer(
                "На какой меняем?",
                reply_markup=await get_start_keyboard(is_choice_skin=True)
            )
        else:
            await call.message.answer(
                "What are we changing to?",
                reply_markup=await get_start_keyboard(is_choice_skin=True, lang='en')
            )
        await state.finish()
