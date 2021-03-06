from datetime import timedelta
from hashlib import scrypt as hashlib_scrypt
from hmac import compare_digest as hmac_compare_digest
from pickle import dumps as pickle_dumps
from pickletools import optimize as pickletools_optimize

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import Command
from aiogram.types import Message, CallbackQuery, ChatActions
from aiogram.utils.markdown import hspoiler
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.exc import SQLAlchemyError
from pgpy import PGPMessage

from config import bot_config
from handlers.states_in_handlers import PasswordStates
from loader import dp, logger_guru, scheduler
from middlewares.throttling import rate_limit
from utils.database_manage.sql.sql_commands import DB_USERS
from utils.keyboards.pass_settings_bk import pass_choice_kb
from utils.misc.other_funcs import delete_marked_message, get_time_now


@logger_guru.catch()
def convert_password_to_enc_object(user_id: int, name_pass: str, password: str) -> bytes:
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


@rate_limit(2, key='pass')
@dp.message_handler(Command('pass'))
async def accept_settings_for_remembering_password(message: Message, state: FSMContext) -> None:
    match lang := await DB_USERS.select_bot_language(telegram_id=(user_id := message.from_user.id)):
        case 'ru':
            text_msg: str = 'Привет, я могу запонить 🔐 твои пароли, для этого мне нужно знать твоё кодовое слово...'
        case _:
            text_msg: str = 'Hello, I can remember 🔐 your passwords, for this I need to know your codeword...'
    await message.delete()
    await message.answer(text_msg)

    await PasswordStates.first()
    async with state.proxy() as data:
        data['user_id'], data['lang'] = user_id, lang


@dp.message_handler(state=PasswordStates.check_personal_code)
async def accept_settings_for_remembering_password(message: Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        user_id, lang = data.values()

    skin = await DB_USERS.select_skin(telegram_id=user_id)
    msg: str = hashlib_scrypt(message.text.encode(), salt=f'{user_id}'.encode(), n=8, r=512, p=4, dklen=32).hex()

    try:
        if check_pass := await DB_USERS.check_personal_pass(telegram_id=user_id):
            if hmac_compare_digest(check_pass, msg):
                await message.answer_sticker(skin.order_accepted.value, disable_notification=True)
                await message.answer('ПРИНЯТО!' if lang == 'ru' else 'ACCEPTED!')

                await PasswordStates.next()
                async with state.proxy() as data:
                    data['lang'] = lang

                tex_msg: str = 'Что ты конкретно хочешь?' if lang == 'ru' else 'What do you specifically want?'
                await message.answer(tex_msg, reply_markup=pass_choice_kb)
            else:
                match lang:
                    case 'ru':
                        await message.answer('НЕВЕРНО! попробуй ещё раз :С\n\n'
                                             'п.с: если твой пароль потерялся, то нашиши в саппорт!\n\n'
                                             '<i>подсказка: /support</i>')
                    case _:
                        await message.answer('WRONG! try again :С\n\n'
                                             'п.с: If your codeword is lost, then write to support!\n\n'
                                             '<i>prompt: /support</i>')
                await state.finish()
        else:
            await DB_USERS.update_personal_pass(telegram_id=user_id, personal_pass=msg)
            await message.answer(
                'Добавила :)\nнапиши его ещё раз.' if lang == 'ru' else
                "Didn't find it on the list, added it:)\nwrite it again."
            )
        await message.delete()
    except SQLAlchemyError as err:
        logger_guru.exception(f'{repr(err)} : in check_personal_code handler!')
        await state.finish()


@dp.callback_query_handler(text='new_pass', state=PasswordStates.successful_auth_for_pass)
async def accept_personal_key(call: CallbackQuery, state: FSMContext) -> None:
    async with state.proxy() as data:
        lang: str = data.get('lang')

    await call.message.answer(
        'Задай имя сохраняемого пароля ...\n (можешь сразу и сам пароль)' if lang == 'ru' else
        'Set the name of the password to be saved ...\n (you can also use the password itself)'
    )
    await call.message.delete_reply_markup()


@dp.message_handler(state=PasswordStates.successful_auth_for_pass)
async def set_name_and_write_pass(message: Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        user_id, lang, name_pass = data.get('user_id'), data.get('lang'), data.get('name')

    msg: str = message.text

    match msg.replace(',', ' ').split():
        case name_pass, password:
            await message.delete()
            enc_pass: bytes = convert_password_to_enc_object(user_id, name_pass, password)
            try:
                await DB_USERS.add_other_info(telegram_id=user_id, name=name_pass, info_for_save=enc_pass)
            except IntegrityError:
                await DB_USERS.update_pass(telegram_id=user_id, name_pass=name_pass, info_for_save=enc_pass)
            await message.answer('Отлично! Записано.' if lang == 'ru' else 'Fine!')
            await state.finish()
        case _:
            if not name_pass:
                async with state.proxy() as data:
                    data['name'] = msg
                await message.delete()
                await message.answer('А теперь пароль :)' if lang == 'ru' else 'And now the password :)')
            else:
                enc_pass: bytes = convert_password_to_enc_object(user_id, name_pass, msg)
                try:
                    await DB_USERS.add_other_info(telegram_id=user_id, name=name_pass, info_for_save=enc_pass)
                except IntegrityError:
                    await DB_USERS.update_pass(telegram_id=user_id, name_pass=name_pass, info_for_save=enc_pass)
                await message.delete()
                await message.answer('Пoлучено, записано!' if lang == 'ru' else 'Received and recorded!')
                await state.finish()


@dp.callback_query_handler(text='receive_pass', state=PasswordStates.successful_auth_for_pass)
async def get_existing_pass(call: CallbackQuery, state: FSMContext) -> None:
    async with state.proxy() as data:
        lang: str = data['lang']

    await call.message.answer('Какое "имя" пароля?' if lang == 'ru' else 'What is the "name" of the password?')
    await call.message.delete_reply_markup()
    await PasswordStates.last()


@dp.message_handler(state=PasswordStates.set_name_pass)
async def get_name_of_the_requested_password(message: Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        user_id, lang = data.values()

    msg: str = message.text.replace(' ', '')
    try:
        if decrypt_password := await DB_USERS.select_pass(name=msg, telegram_id=user_id):
            very_useful_thing: str = hashlib_scrypt(msg.encode(), salt=f'{user_id}'.encode(),
                                               n=8, r=512, p=4, dklen=16).hex()
            password: str = decrypt_password.decrypt(very_useful_thing).message
            text_msg: str = (
                f'НАШЛА! вот пароль с именем <b><code>{msg}</code></b> :\n\n'
                f'{hspoiler(password)}\n\n'
                f'у тебя 10 секунд чтобы его скопировать !' if lang == 'ru' else
                f'FOUND! here is the password with the name <b><code>{msg}</code></b> :\n\n'
                f'{hspoiler(password)}\n\n'
                f'after 10 seconds it will be deleted !'
            )

            removing_msg: Message = await message.answer(text_msg)
            delete_time: str = (get_time_now(bot_config.time_zone) + timedelta(seconds=10)).strftime('%Y-%m-%d %H:%M:%S')
            scheduler.add_job(
                delete_marked_message, id=f'del_msg_{user_id}',
                args=(removing_msg.message_id, message.chat.id), trigger='date',
                replace_existing=True, run_date=delete_time, timezone="Europe/Moscow"
            )
            await message.delete()
    except NoResultFound:
        logger_guru.warning(f'{user_id=} entering an invalid password name!')
        await message.delete()
        await message.answer_chat_action(ChatActions.TYPING)
        await message.answer(
            f'Не найден пароль с именем {hspoiler(message.text)} 😕' if lang == 'ru' else
            f"Couldn't find a password with {hspoiler(message.text)} 😕"
        )
    finally:
        await state.finish()
