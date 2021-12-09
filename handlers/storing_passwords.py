from asyncio import sleep as asyncio_sleep
from hashlib import scrypt as hashlib_scrypt
from sqlite3 import Error as sqlite3_Error

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import Command
from aiogram.types import Message, CallbackQuery

from loader import dp, db, logger_guru
from utils.keyboards.pass_settings_bk import pass_choice_kb




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
        if check_pass := db.check_personal_pass(telegram_id=user_id)[0]:
            if check_pass == msg:
                await message.answer('ПРИНЯТО!')
                await state.set_state('successful_auth_for_pass')
                await message.answer('Что ты конкретно хочешь?', reply_markup=pass_choice_kb)
            else:
                await message.answer('НЕ ВЕРНО! попробуй ещё раз :С\n\n'
                                     'п.с: если твой пароль потерялся, то нашиши в саппорт!\n'
                                     'подсказка: /support')
                await state.finish()
        else:
            db.update_personal_pass(telegram_id=user_id, personal_pass=msg)
            await message.answer('Не нашла его в списке, добавила :)\nнапиши его ещё раз.')
        await message.delete()
    except sqlite3_Error as err:
        logger_guru.warning(f'{repr(err)} : Error in check_personal_code handler!')
        await state.finish()


@dp.callback_query_handler(text='new_pass', state='successful_auth_for_pass')
async def accept_personal_key(call: CallbackQuery):
    await call.message.answer(f'Задай имя сохраняемого пароля ...\n'
                              f'(можешь сразу и сам пароль)')


@dp.message_handler(state='successful_auth_for_pass')
async def set_name_and_write_pass(message: Message, state: FSMContext):
    msg: str = message.text

    async with state.proxy() as data:
        is_temp: bool = data.get('temp')

    match msg.replace(',', ' ').split():
        case name_pass, password:
            db.add_pass(telegram_id=message.from_user.id, name_pass=name_pass, pass_items=password)
            await message.answer(f'Отлично! записала.')
            await message.delete()
            await state.finish()
        case _:
            if not is_temp:
                await message.answer(f'так... имя: {msg} записала, теперь сам пароль!')
                async with state.proxy() as data:
                    data['is_temp']: bool = True
            else:
                password: str = message.text
                await message.answer(f'Пoлучила, записала! {password}')
                await state.finish()


@dp.callback_query_handler(text='receive_pass', state='successful_auth_for_pass')
async def get_existing_pass(call: CallbackQuery, state: FSMContext):
    await call.message.answer('Какое имя пароля?')
    await call.message.edit_reply_markup()
    await state.set_state('set_name_pass')


@dp.message_handler(state='set_name_pass')
async def get_name_of_the_requested_password(message: Message, state: FSMContext):
    msg: str = message.text.replace(' ','')
    try:
        if password := db.select_pass(name_pass=msg, telegram_id=message.from_user.id):
            await message.answer(f'НАШЛА! вот пароль с именем {msg} : {password[0]}\n'
                             f'у тебя 20 секунд чтобы его скопировать !')

            await asyncio_sleep(20)
            await message.bot.delete_message(message.chat.id, message.message_id + 1)
            await message.delete()
            await message.answer('Надеюсь, ты успел записать :)')

    except:
        await message.answer('Не нашла пароля с таким именем :С')
    finally:
        await state.finish()



