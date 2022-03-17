from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery
from sqlalchemy.exc import NoResultFound

from loader import dp, logger_guru
from utils.database_manage.sql.sql_commands import DB_USERS
from utils.keyboards.admins_tools_kb import tools_choice_kb
from utils.misc.notify_users import send_a_message_to_all_users


@dp.message_handler(Command('admin_tools'))
async def go_to_admin_panel(message: Message, state: FSMContext) -> None:
    lang: str = await DB_USERS.select_bot_language(telegram_id=message.from_user.id)

    await message.answer(
        'Чего изволите?' if lang == 'ru' else 'What would you like?', reply_markup=tools_choice_kb
    )
    await state.set_state('admin_in_action')
    async with state.proxy() as data:
        data['lang']: str = lang


@dp.callback_query_handler(text={'reset_user_codeword', 'make_newsletter'}, state='admin_in_action')
async def choose_an_action(call: CallbackQuery, state: FSMContext) -> None:
    async with state.proxy() as data:
        lang: str = data.get('lang')

    if call.data == 'reset_user_codeword':
        await call.message.answer('id пользователя?' if lang == 'ru' else 'user id?')
        await state.set_state('accept_user_id')
    elif call.data == 'make_newsletter':
        await call.message.answer('текст рассылки?' if lang == 'ru' else 'mailing text?')
        await state.set_state('receiving_mailing_text')

    await call.message.delete_reply_markup()


@dp.message_handler(state='accept_user_id')
async def take_user_id(message: Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        lang: str = data.get('lang')
    try:
        if await DB_USERS.check_personal_pass(telegram_id=message.text):
            await DB_USERS.update_personal_pass(telegram_id=message.text, personal_pass=None)
            await message.answer('СДЕЛАНО!' if lang == 'ru' else 'MADE!')
    except NoResultFound:
        logger_guru.exception('Failed attempt to reset the code word!')
        await message.reply(
            'Что-то пошло не так...смотри логи' if lang == 'ru' else 'Something went wrong...look at the logs'
        )
    finally:
        await state.finish()


@dp.message_handler(state='receiving_mailing_text')
async def make_newsletter_to_all_users(message: Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        lang: str = data.get('lang')

    if not (result := await send_a_message_to_all_users(msg=message.text)):
        await message.answer('Готово!' if lang == 'ru' else 'YAHOO!')
    else:
        await message.answer(
            f'Что-то пошло не так: {result}' if lang == 'ru' else
            f'Something went wrong: {result}'
        )
    await state.finish()
