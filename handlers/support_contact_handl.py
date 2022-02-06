from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery

from loader import dp
from middlewares.throttling import rate_limit
from utils.database_manage.sql.sql_commands import select_bot_language, select_lang_and_skin
from utils.keyboards.support_contact_kb import sup_kb, sup_cb


@rate_limit(5)
@dp.message_handler(Command('support'), state='*')
async def contact_support_by_message(message: Message, state: FSMContext):
    user_id: int = message.from_user.id
    lang, skin = await select_lang_and_skin(telegram_id=user_id)

    text_msg: str = (
        'Хочешь написать создателю?' if lang == 'ru' else 'Do you want to write to the creator?'
    )
    kb = await sup_kb()
    await message.answer_sticker(skin.fear.value)
    await message.answer(text_msg, reply_markup=kb)
    await state.finish()
    await message.delete()


@dp.callback_query_handler(sup_cb.filter())
async def send_to_sup(call: CallbackQuery, state: FSMContext, callback_data: dict):
    await state.set_state('msg_for_admin')
    await state.update_data(second_id=callback_data.get('telegram_id'))
    await call.message.delete_reply_markup()
    await call.message.answer(
        'пиши ...' if await select_bot_language(telegram_id=call.from_user.id) == 'ru' else 'write ...'
    )


@dp.message_handler(state='msg_for_admin')
async def get_message(message: Message, state: FSMContext):
    async with state.proxy() as data:
        second_id: str = data.get('second_id')
    lang: str = await select_bot_language(telegram_id=message.from_user.id)
    await message.bot.send_message(
        second_id,
        'Тебе пришло сообщение ->' if lang == 'ru' else
        'You received a message ->'
    )
    kb = await sup_kb(telegram_id=message.from_user.id)
    await message.copy_to(second_id, reply_markup=kb)
    await state.reset_state()

    await message.answer('Сообщение отправлено!' if lang == 'ru' else 'Message sent!')
