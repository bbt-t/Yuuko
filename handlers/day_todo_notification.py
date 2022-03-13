from re import match as re_match

from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery

from handlers.states_in_handlers import UserSettingStates
from loader import dp, logger_guru, scheduler
from utils.database_manage.sql.sql_commands import DB_USERS
from utils.keyboards.choice_voice_todo import choice_voice_todo_keyboard
from utils.keyboards.yes_no import yes_no_choice_kb
from utils.misc.notify_users import send_todo_msg


@dp.callback_query_handler(text='set_time_todo', state=UserSettingStates.settings)
async def late_day_todo_notification(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        lang: str = data.get('lang')

    await call.message.answer(
        'Когда напоминать о делах?' if lang == 'ru' else 'When to remind about "todo"?'
    )
    await call.message.delete()

    await UserSettingStates.next()


@dp.message_handler(state=UserSettingStates.time_todo)
async def question_set_time_todo(message: Message, state: FSMContext):
    skin = await DB_USERS.select_skin(telegram_id=message.from_user.id)
    msg: str = ''.join(let for let in message.text if let.isnumeric())

    async with state.proxy() as data:
        lang: str = data.get('lang')
        if not (msg and 2 <= len(msg) <= 4):
            await state.finish()
            return await message.reply(
                'Напиши мне <code>время</code> ... попробуй ещё раз.' if lang == 'ru' else
                'Text me <code>time</code> ... try again.'
            )
        else:
            data['msg'] = msg
    await message.answer_sticker(skin.love_you.value, disable_notification=True)
    await message.answer(
        'а можно я тебе буду голосовые сообщения слать?' if lang == 'ru' else
        'Can I send you voice messages?',
        reply_markup=choice_voice_todo_keyboard
    )


@dp.callback_query_handler(state=UserSettingStates.time_todo)
async def start_set_time_todo(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        lang, text = data.get('lang'), data.get('msg')

    await call.message.delete_reply_markup()
    skin, choice = await DB_USERS.select_skin(user_id := call.from_user.id), call.data

    if re_match(r'^([01]\d|2[0-3])?([0-5]\d)$', text := text.zfill(4)[:4]):
        try:
            is_voice = True if choice != 'choice_voice_no' else False

            scheduler.add_job(send_todo_msg, 'cron', day_of_week='mon-sun', id=f'job_send_todo_{user_id}',
                              hour=text[:2], minute=text[-2:], end_date='2025-05-30', args=(user_id, is_voice),
                              misfire_grace_time=30, replace_existing=True, timezone="Europe/Moscow")

            logger_guru.info(f"{user_id=} changed the notification time")
            await call.message.answer_sticker(skin.great.value, disable_notification=True)
            await call.message.answer('Сделано !')
        except KeyError:
            logger_guru.exception(f'{user_id=} : ERROR ADD WEATHER JOB')
        finally:
            await state.finish()
    else:
        await call.message.answer_sticker(skin.i_do_not_understand.value, disable_notification=True)
        await call.message.answer('Не понятно что написано, попробуй ещё раз ...')
        await state.finish()

    if not any(job.id == f'weather_add_id_{user_id}' for job in scheduler.get_jobs()):
        await call.message.answer('Я могу ещё писать тебе о погоде...', reply_markup=yes_no_choice_kb)


@dp.callback_query_handler(text='weather_add')
async def weather_accept(call: CallbackQuery, state: FSMContext):
    lang: str = await DB_USERS.select_bot_language(telegram_id=call.from_user.id)

    await call.message.delete_reply_markup()
    await call.message.edit_text('время?' if lang == 'ru' else 'time?')

    await UserSettingStates.weather_on.set()
    async with state.proxy() as data:
        data['lang'] = lang
