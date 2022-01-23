from asyncio import sleep as asyncio_sleep
from hashlib import scrypt as hashlib_scrypt
from hmac import compare_digest as hmac_compare_digest
from pickle import dumps as pickle_dumps
from pickletools import optimize as pickletools_optimize
from sqlite3 import Error as sqlite3_Error

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import Command
from aiogram.types import Message, CallbackQuery
from pgpy import PGPMessage

from loader import dp, logger_guru
from middlewares.throttling import rate_limit
from utils.database_manage.sql.sql_commands import check_personal_pass, update_personal_pass, add_other_info, select_pass
from utils.keyboards.pass_settings_bk import pass_choice_kb
from utils.misc.enums_data import SendStickers


@logger_guru.catch()
async def convert_password_to_enc_object(user_id: int, name_pass: str, password: str) -> bytes:
    """
    Encrypts password and serializes for storage
    :param user_id: ID who wrote
    :param name_pass: given password name
    :param password: password
    :return: pickle object
    """
    very_useful_thing: str = hashlib_scrypt(
        name_pass.encode(), salt=f'{user_id}'.encode(), n=8, r=512, p=4, dklen=16).hex()
    encrypt_password = PGPMessage.new(password.encode()).encrypt(very_useful_thing)
    serialized_object: bytes = pickletools_optimize(pickle_dumps(encrypt_password))

    return serialized_object


@rate_limit(5)
@dp.message_handler(Command('pass'))
async def accept_settings_for_remembering_password(message: Message, state: FSMContext):
    await message.answer('Привет, я могу запонить твои пароли, '
                         'для этого мне нужно знать твоё кодовое слово...')
    await state.set_state('check_personal_code')
    await message.delete()


@dp.message_handler(state='check_personal_code')
async def accept_settings_for_remembering_password(message: Message, state: FSMContext):
    user_id: int = message.from_user.id
    msg: str = hashlib_scrypt(message.text.encode(), salt=f'{user_id}'.encode(), n=8, r=512, p=4, dklen=32).hex()

    try:
        if check_pass := await check_personal_pass(id=user_id):
            if hmac_compare_digest(check_pass, msg):
                await message.reply_sticker(SendStickers.order_accepted.value)
                await message.answer('ПРИНЯТО!')
                await state.set_state('successful_auth_for_pass')
                await message.answer('Что ты конкретно хочешь?', reply_markup=pass_choice_kb)
            else:
                await message.answer('НЕ ВЕРНО! попробуй ещё раз :С\n\n'
                                     'п.с: если твой пароль потерялся, то нашиши в саппорт!\n'
                                     'подсказка: /support')
                await state.finish()
        else:
            await update_personal_pass(id=user_id, personal_pass=msg)
            await message.answer('Не нашла его в списке, добавила :)\nнапиши его ещё раз.')
        await message.delete()
    except sqlite3_Error as err:
        logger_guru.warning(f'{repr(err)} : Error in check_personal_code handler!')
        await state.finish()


@dp.callback_query_handler(text='new_pass', state='successful_auth_for_pass')
async def accept_personal_key(call: CallbackQuery):
    await call.message.answer(f'Задай имя сохраняемого пароля ...\n'
                              f'(можешь сразу и сам пароль)')
    await call.message.delete_reply_markup()


@dp.message_handler(state='successful_auth_for_pass')
async def set_name_and_write_pass(message: Message, state: FSMContext):
    msg: str = message.text
    user_id: int = message.from_user.id

    async with state.proxy() as data:
        name_pass: str = data.get('name')

    match msg.replace(',', ' ').split():
        case name_pass, password:
            await message.delete()
            enc_pass: bytes = await convert_password_to_enc_object(user_id, name_pass, password)
            await add_other_info(id=user_id, name=name_pass, info_for_save=enc_pass)
            await message.answer(f'Отлично! записала.')
            await state.finish()
        case _:
            if not name_pass:
                async with state.proxy() as data:
                    data['name']: str = msg
                await message.delete()
                await message.answer('А теперь пароль :)')
            else:
                enc_pass: bytes = await convert_password_to_enc_object(user_id, name_pass, msg)
                await add_other_info(id=user_id, name=name_pass, info_for_save=enc_pass)
                await message.delete()
                await message.answer(f'Пoлучила, записала!')
                await state.finish()


@dp.callback_query_handler(text='receive_pass', state='successful_auth_for_pass')
async def get_existing_pass(call: CallbackQuery, state: FSMContext):
    await call.message.answer('Какое имя пароля?')
    await call.message.delete_reply_markup()
    await state.set_state('set_name_pass')


@dp.message_handler(state='set_name_pass')
async def get_name_of_the_requested_password(message: Message, state: FSMContext):
    msg: str = message.text.replace(' ', '')
    user_id: int = message.from_user.id
    try:
        if decrypt_password := await select_pass(name=msg, id=user_id):
            very_useful_thing = hashlib_scrypt(msg.encode(), salt=f'{user_id}'.encode(),
                                               n=8, r=512, p=4, dklen=16).hex()
            password: str = decrypt_password.decrypt(very_useful_thing).message
            removing_msg = await message.answer(
                f'НАШЛА! вот пароль с именем {msg} : {password}\n'
                f'у тебя 20 секунд чтобы его скопировать !'
            )
            await asyncio_sleep(20)
            await removing_msg.delete()
            await message.delete()

            await message.answer('Надеюсь, ты успел записать :)')
    except:
        await message.answer('Не нашла пароля с таким именем :С')
    finally:
        await state.finish()
