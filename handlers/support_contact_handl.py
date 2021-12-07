from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from loader import dp
from utils.keyboards.support_contact_kb import sup_kb, sup_cb




@dp.message_handler(Command('support'))
async def contact_support_by_message(message: Message):
    kb = await sup_kb()
    await message.reply_sticker('CAACAgIAAxkBAAEDbxphr6Avra8WTksfENEkK1GuHIpwpQACZAEAAhAabSJJXz3XqubCyiME')
    await message.answer('Хочешь написать создателю?)', reply_markup=kb)


@dp.callback_query_handler(sup_cb.filter())
async def send_to_sup(call: CallbackQuery, state: FSMContext, callback_data):
    await state.set_state('msg_for_admin')
    await state.update_data(second_id=callback_data.get('telegram_id'))
    await call.message.edit_reply_markup()

    await call.message.answer('пиши ...')


@dp.message_handler(state='msg_for_admin')
async def get_message(message: Message, state: FSMContext):
    async with state.proxy() as data:
        second_id: str = data['second_id']

    await message.bot.send_message(second_id, f'Тебе письмо ->')
    kb = await sup_kb(telegram_id=message.from_user.id)
    await message.copy_to(second_id, reply_markup=kb)
    await state.reset_state()

    await message.answer('Сообщение отправлено!')
