from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from handlers.states_in_handlers import UserSettingStates
from loader import dp
from utils.keyboards.start_handl_choice_kb import choice_of_assistant_kb_ru, choice_of_assistant_kb_en


@dp.callback_query_handler(text='set_skin', state=UserSettingStates.settings)
async def choose_a_sticker_pack(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        lang: str = data.get('lang')

    if lang == 'ru':
        await call.message.answer("На какой меняем?", reply_markup=choice_of_assistant_kb_ru)
    else:
        await call.message.answer("What are we changing to?", reply_markup=choice_of_assistant_kb_en)
    await state.finish()
