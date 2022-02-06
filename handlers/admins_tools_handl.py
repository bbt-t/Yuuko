from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery
from sqlalchemy.exc import NoResultFound

from loader import dp, logger_guru
from utils.database_manage.sql.sql_commands import update_personal_pass, check_personal_pass, select_bot_language
from utils.keyboards.admins_tools_kb import tools_choice_kb


@dp.message_handler(Command('reset_personal_pass'))
async def reset_user_passcode(message: Message, state: FSMContext):
    lang: str = await select_bot_language(telegram_id=message.from_user.id)

    await message.answer('Чего изволите?', reply_markup=tools_choice_kb)

    await state.set_state('admin_in_action')
    async with state.proxy() as data:
        data['lang'] = lang


@dp.callback_query_handler(text='reset_user_codeword', state='admin_in_action')
async def get_horoscope(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        lang: str = data.get('lang')

    await call.message.delete_reply_markup()
    await call.message.answer('id пользователя?' if lang == 'ru' else 'user id?')
    await state.set_state('accept_user_id')


@dp.message_handler(state='accept_user_id')
async def take_user_id(message: Message, state: FSMContext):
    async with state.proxy() as data:
        lang: str = data.get('lang')
    try:
        if await check_personal_pass(telegram_id=message.text):
            await update_personal_pass(telegram_id=message.text, personal_pass=None)
            await message.answer('СДЕЛАНО!' if lang == 'ru' else 'MADE!')
    except NoResultFound:
        logger_guru.exception('Failed attempt to reset the code word!')
        await message.reply(
            'Что-то пошло не так...смотри логи' if lang == 'ru' else 'Something went wrong...look at the logs'
        )
    finally:
        await state.finish()
