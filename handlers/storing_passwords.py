from datetime import timedelta
from hashlib import scrypt as hashlib_scrypt
from hmac import compare_digest as hmac_compare_digest
from pickle import dumps as pickle_dumps
from pickletools import optimize as pickletools_optimize

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import Command
from aiogram.types import Message, CallbackQuery
from sqlalchemy.exc import IntegrityError, NoResultFound
from pgpy import PGPMessage

from config import time_zone
from loader import dp, logger_guru, scheduler
from middlewares.throttling import rate_limit
from utils.database_manage.sql.sql_commands import (check_personal_pass, update_personal_pass,add_other_info,
                                                    select_pass, update_pass, select_skin, select_bot_language)
from utils.keyboards.pass_settings_bk import pass_choice_kb
from utils.misc.other_funcs import delete_marked_message, get_time_now


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
        name_pass.encode(),
        salt=f'{user_id}'.encode(),
        n=8, r=512, p=4, dklen=16
    ).hex()
    encrypt_password = PGPMessage.new(password.encode()).encrypt(very_useful_thing)
    serialized_object: bytes = pickletools_optimize(pickle_dumps(encrypt_password))

    return serialized_object


@rate_limit(5, key='pass')
@dp.message_handler(Command('pass'))
async def accept_settings_for_remembering_password(message: Message, state: FSMContext):
    user_id: int = message.from_user.id
    match lang := await select_bot_language(telegram_id=user_id):
        case 'ru':
            text_msg: str = 'Привет, я могу запонить 🔐 твои пароли, для этого мне нужно знать твоё кодовое слово...'
        case _:
            text_msg: str = 'Hello, I can remember 🔐 your passwords, for this I need to know your codeword...'
    await message.delete()
    await message.answer(text_msg)
    await state.set_state('check_personal_code')
    async with state.proxy() as data:
        data['user_id']: str = user_id
        data['lang']: str = lang



@dp.message_handler(state='check_personal_code')
async def accept_settings_for_remembering_password(message: Message, state: FSMContext):
    async with state.proxy() as data:
        user_id, lang = data.values()

    skin = await select_skin(telegram_id=user_id)
    msg: str = hashlib_scrypt(message.text.encode(), salt=f'{user_id}'.encode(), n=8, r=512, p=4, dklen=32).hex()

    try:
        if check_pass := await check_personal_pass(telegram_id=user_id):
            if hmac_compare_digest(check_pass, msg):
                await message.answer_sticker(skin.order_accepted.value)
                await message.answer('ПРИНЯТО!' if lang == 'ru' else 'ACCEPTED!')
                await state.set_state('successful_auth_for_pass')
                async with state.proxy() as data:
                    data['lang']: str = lang
                tex_msg: str = 'Что ты конкретно хочешь?' if lang == 'ru' else 'What do you specifically want?'
                await message.answer(tex_msg, reply_markup=pass_choice_kb)
            else:
                match lang:
                    case 'ru':
                        await message.answer('НЕВЕРНО! попробуй ещё раз :С\n\n'
                                             'п.с: если твой пароль потерялся, то нашиши в саппорт!\n'
                                             'подсказка: /support')
                    case _:
                        await message.answer('WRONG! try again :С\n\n'
                                             'п.с: If your codeword is lost, then write to support!\n'
                                             'подсказка: /support')
                await state.finish()
        else:
            await update_personal_pass(telegram_id=user_id, personal_pass=msg)
            await message.answer(
                'Добавила :)\nнапиши его ещё раз.' if lang == 'ru' else
                "Didn't find it on the list, added it:)\nwrite it again."
            )
        await message.delete()
    except:
        logger_guru.exception('Error in check_personal_code handler!')
        await state.finish()


@dp.callback_query_handler(text='new_pass', state='successful_auth_for_pass')
async def accept_personal_key(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        lang: str = data.get('lang')
    await call.message.answer(
        'Задай имя сохраняемого пароля ...\n (можешь сразу и сам пароль)' if lang == 'ru' else
        'Set the name of the password to be saved ...\n (you can also use the password itself)'
    )
    await call.message.delete_reply_markup()


@dp.message_handler(state='successful_auth_for_pass')
async def set_name_and_write_pass(message: Message, state: FSMContext):
    msg: str = message.text

    async with state.proxy() as data:
        user_id, lang, name_pass = data.get('user_id'), data.get('lang'), data.get('name')

    match msg.replace(',', ' ').split():
        case name_pass, password:
            await message.delete()
            enc_pass: bytes = await convert_password_to_enc_object(user_id, name_pass, password)
            try:
                await add_other_info(telegram_id=user_id, name=name_pass, info_for_save=enc_pass)
            except IntegrityError:
                await update_pass(telegram_id=user_id, name_pass=name_pass, info_for_save=enc_pass)
            await message.answer('Отлично! записино.' if lang == 'ru' else 'Fine! wrote down.')
            await state.finish()
        case _:
            if not name_pass:
                async with state.proxy() as data:
                    data['name']: str = msg
                await message.delete()
                await message.answer('А теперь пароль :)' if lang == 'ru' else 'And now the password :)')
            else:
                enc_pass: bytes = await convert_password_to_enc_object(user_id, name_pass, msg)
                try:
                    await add_other_info(telegram_id=user_id, name=name_pass, info_for_save=enc_pass)
                except IntegrityError:
                    await update_pass(telegram_id=user_id, name_pass=name_pass, info_for_save=enc_pass)
                await message.delete()
                await message.answer('Пoлучено, записано!' if lang == 'ru' else 'Received and recorded!')
                await state.finish()


@dp.callback_query_handler(text='receive_pass', state='successful_auth_for_pass')
async def get_existing_pass(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        lang: str = data['lang']
    await call.message.answer('Какое "имя" пароля?' if lang == 'ru' else 'What is the "name" of the password?')
    await call.message.delete_reply_markup()
    await state.set_state('set_name_pass')


@dp.message_handler(state='set_name_pass')
async def get_name_of_the_requested_password(message: Message, state: FSMContext):
    async with state.proxy() as data:
        user_id, lang = data.values()
    msg: str = message.text.replace(' ', '')

    try:
        if decrypt_password := await select_pass(name=msg, telegram_id=user_id):
            very_useful_thing = hashlib_scrypt(msg.encode(), salt=f'{user_id}'.encode(),
                                               n=8, r=512, p=4, dklen=16).hex()
            password: str = decrypt_password.decrypt(very_useful_thing).message
            text_msg: str = (
                f'НАШЛА! вот пароль с именем {msg} : {password}\n'
                f'у тебя 10 секунд чтобы его скопировать !' if lang == 'ru' else
                f'FOUND! here is the password with the name {msg} : {password}\n'
                f'after 10 seconds it will be deleted !'
            )

            removing_msg: Message = await message.answer(text_msg)
            delete_time: str = (get_time_now(time_zone) + timedelta(seconds=10)).strftime('%Y-%m-%d %H:%M:%S')
            scheduler.add_job(
                delete_marked_message, id=f'del_msg_{user_id}',
                args=(removing_msg.message_id, message.chat.id), trigger='date',
                replace_existing=True, run_date=delete_time, timezone="Europe/Moscow"
            )
            await message.delete()
    except NoResultFound:
        logger_guru.warning(f'{user_id=} entering an invalid password name.')
        await message.answer(
            'Не найден пароль с таким именем 😕' if lang == 'ru' else "Couldn't find a password with that name :C"
        )
    finally:
        await state.finish()
