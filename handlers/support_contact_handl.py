from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery

from utils.misc.enums_data import SendStickers
from loader import dp
from middlewares.throttling import rate_limit
from utils.keyboards.support_contact_kb import sup_kb, sup_cb




@rate_limit(5)
@dp.message_handler(Command('support'), state='*')
async def contact_support_by_message(message: Message, state: FSMContext):
    kb = await sup_kb()
    await message.answer_sticker(SendStickers.fear.value)
    await message.answer(
        'Хочешь написать создателю?' if message.from_user.language_code == 'ru' else
        'Do you want to write to the creator?', reply_markup=kb
    )
    await state.finish()
    await message.delete()


@dp.callback_query_handler(sup_cb.filter())
async def send_to_sup(call: CallbackQuery, state: FSMContext, callback_data: dict):
    await state.set_state('msg_for_admin')
    await state.update_data(second_id=callback_data.get('telegram_id'))
    await call.message.delete_reply_markup()
    await call.message.answer('пиши ...')


@dp.message_handler(state='msg_for_admin')
async def get_message(message: Message, state: FSMContext):
    async with state.proxy() as data:
        second_id: str = data.get('second_id')

    await message.bot.send_message(second_id, 'Тебе пришло сообщение ->')
    kb = await sup_kb(telegram_id=message.from_user.id)
    await message.copy_to(second_id, reply_markup=kb)
    await state.reset_state()

    await message.answer('Сообщение отправлено!')
