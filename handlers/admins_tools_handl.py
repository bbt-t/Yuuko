from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery


from loader import dp, logger_guru
from utils.database_manage.sql.sql_commands import update_personal_pass
from utils.keyboards.admins_tools_kb import tools_choice_kb


@dp.message_handler(Command('reset_personal_pass'))
async def reset_user_passcode(message: Message, state: FSMContext):
    lang: str = message.from_user.language_code
    await message.answer('Чего изволите?', reply_markup=tools_choice_kb)

    await state.set_state('admin_in_action')
    async with state.proxy() as data:
        data['lang'] = lang


@dp.callback_query_handler(text='reset_user_codeword', state='admin_in_action')
async def get_horoscope(call: CallbackQuery, state: FSMContext):
    await call.message.delete_reply_markup()
    await call.message.answer('id пользователя?')
    await state.set_state('accept_user_id')


@dp.message_handler(state='accept_user_id')
async def take_user_id(message: Message, state: FSMContext):
    try:
        await update_personal_pass(message.text, None)
    except:
        logger_guru.warning('Failed attempt to reset the code word !')
        await message.reply('Что-то пошло не так...')
    else:
        await message.answer('СДЕЛАНО!')
    finally:
        await state.finish()
