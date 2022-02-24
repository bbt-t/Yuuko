from asyncio import sleep as asyncio_sleep

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import Message, CallbackQuery, ChatActions
from sqlalchemy.exc import IntegrityError

from config import time_zone
from loader import dp, logger_guru, scheduler
from middlewares.throttling import rate_limit
from utils.database_manage.sql.sql_commands import (add_user, update_birthday, select_skin,
                                                    update_bot_skin, select_bot_language, select_lang_and_skin)
from utils.keyboards.calendar import calendar_bot_ru, calendar_bot_en, calendar_cb
from utils.keyboards.start_handl_choice_kb import (initial_setup_choice_kb_ru, choice_of_assistant_kb_ru,
                                                   choice_of_assistant_kb_en, initial_setup_choice_kb_en)
from utils.misc.enums_data import BotSkins
from utils.misc.notify_users import auth
from utils.misc.other_funcs import get_time_now


@rate_limit(5, key='start')
@dp.message_handler(CommandStart())
@auth
async def start_working_with_bot(message: Message):
    """
    Such a response will be sent at the start of communication (/start)
    """
    user_id, name = message.from_user.id, message.from_user.full_name
    lang: str = message.from_user.language_code

    try:
        await add_user(telegram_id=user_id, lang=lang)
    except IntegrityError:
        logger_guru.opt(exception=True).critical(f'{user_id=} : Integrity Error in start handler!')

    await message.answer_sticker(BotSkins.cloud.value.welcome.value, disable_notification=True)
    await dp.bot.send_chat_action(user_id, ChatActions.TYPING)
    await asyncio_sleep(2)

    match await select_bot_language(telegram_id=user_id):
        case 'ru':
            text_msg: str = f"Привет, {name}!\n\nвыбери в какой 'форме' мне быть"
            await message.answer(text_msg, reply_markup=choice_of_assistant_kb_ru)
        case _:
            text_msg: str = f"Hi, {name}!\n\nchoose in what 'shape' I be"
            await message.answer(text_msg, reply_markup=choice_of_assistant_kb_en)


@dp.callback_query_handler(text=['neko', 'chan', 'cloud'])
async def choose_skin_for_the_bot(call: CallbackQuery):
    user_id: int = call.from_user.id
    await update_bot_skin(telegram_id=user_id, skin=getattr(BotSkins, call.data))
    skin = await select_skin(telegram_id=user_id)

    await call.message.delete_reply_markup()
    await call.message.answer_sticker(skin.great.value, disable_notification=True)

    if not any(str(sch.id).endswith(f'{user_id}') for sch in scheduler.get_jobs()):
        if await select_bot_language(telegram_id=user_id) == 'ru':
            await call.message.answer(
                'Отлично!)\nп.с:<s> ты в любой момент можешь сменить напарника</s>\n\n'
                'а теперь настройки!', reply_markup=initial_setup_choice_kb_ru
            )
        else:
            await call.message.answer(
                'Fine!)\nyou can change your partner at any time if suddenly I don’t suit you 😰\n\n'
                'and now settings!', reply_markup=initial_setup_choice_kb_en
            )
    else:
        await call.message.answer('YAHOO! ^^')


@dp.callback_query_handler(text='set_birthday')
async def indicate_date_of_birth(call: CallbackQuery, state: FSMContext):
    lang, skin = await select_lang_and_skin(call.from_user.id)

    text_msg: str = (
        'Укажи свой ДР (настоящий, его всё равно никто не увидит кроме меня 😏' if lang == 'ru' else
        'Specify your DR (real, no one will see it except me anyway 😏'
    )
    removing_msg: Message = await call.message.answer(text_msg)

    await call.message.answer_sticker(skin.seeking.value, disable_notification=True)
    if lang == 'ru':
        await call.message.edit_reply_markup(await calendar_bot_ru.enable())
    else:
        await call.message.edit_reply_markup(await calendar_bot_en.enable())

    await state.set_state('set_birthday_and_todo')
    async with state.proxy() as data:
        data['lang']: str = lang
        data['removing_msg_id'] = removing_msg.message_id


@dp.callback_query_handler(calendar_cb.filter(), state='set_birthday_and_todo')
async def birthday_simple_calendar(call: CallbackQuery, callback_data, state: FSMContext):
    async with state.proxy() as data:
        lang, removing_msg_id = data.values()

    selected, date = (await calendar_bot_ru.process_selection(call, callback_data) if lang == 'ru' else
                      await calendar_bot_en.process_selection(call, callback_data))

    if date and selected:
        if date > get_time_now(time_zone).date():
            if lang == 'ru':
                await call.answer('Выбрать можно только на сегодня и позже !', show_alert=True)
                await call.message.answer(
                    'Ты не можешь выбрать эту дату!', reply_markup=await calendar_bot_ru.enable()
                )
            else:
                await call.answer('You can only choose today and later!', show_alert=True)
                await call.message.answer(
                    "You can't choose this date!", reply_markup=await calendar_bot_ru.enable()
                )
        else:
            await update_birthday(telegram_id=call.from_user.id, birthday=date)
            await dp.bot.delete_message(message_id=removing_msg_id, chat_id=call.message.chat.id)
            await call.message.answer(
                'В какое время спрашивать тебя о "делах"?' if lang == 'ru' else
                'What time should I ask you about planned activities?')
            await state.set_state('set_time_todo')


@dp.callback_query_handler(text='cancel', state='*')
async def exit_handling(call: CallbackQuery, state: FSMContext):
    lang, skin = await select_lang_and_skin(user_id := call.from_user.id)

    await dp.bot.send_chat_action(user_id, ChatActions.TYPING)
    await call.message.answer_sticker(skin.sad_ok.value, disable_notification=True)
    await asyncio_sleep(1)
    text_msg: str = (
        'ЖАЛЬ :С если что мои команды можно подглядеть через слеш (/)' if lang == 'ru' else
        'SORRY :C if you change your mind, you can see my commands through a forward slash (/)'
    )
    await dp.bot.answer_callback_query(call.id, text_msg, show_alert=True)
    await call.message.delete_reply_markup()
    await state.finish()
