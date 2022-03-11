from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ContentType

from config import work_with_api
from loader import dp, logger_guru
from middlewares.throttling import rate_limit
from utils.database_manage.sql.sql_commands import DB_USERS
from utils.misc.other_funcs import cpu_bound_run_func
from utils.work_with_speech.speech_to_text_on_their_own import recognize_locally
from utils.work_with_speech.speech_to_text_yandex import recognize_speech_by_ya


@rate_limit(5)
@dp.message_handler(content_types=ContentType.VOICE)
async def determine_further_path(message: Message, state: FSMContext):
    file_id: str = message.voice.file_id
    try:
        msg: bytes = await message.bot.download_file_by_id(file_id)
        text: str = await recognize_speech_by_ya(
            msg, work_with_api['YANDEX']['FOLDER_ID'], work_with_api['YANDEX']['API_YA_STT']
        )
        if not text:
            raise AttributeError('BAD REQUEST')
    except:
        logger_guru.exception(f'{message.from_user.id} : unsuccessful request STT YANDEX!')

        name_file: str = f"{file_id}.ogg"
        file_path = (await message.bot.get_file(file_id)).file_path
        await message.bot.download_file(file_path, name_file)
        text: str = await cpu_bound_run_func(recognize_locally, name_file)

    if any(let.lower().startswith('пого') for let in text.split()):
        lang = await DB_USERS.select_bot_language(telegram_id=message.from_user.id)
        await message.answer(
            'Давай настроим оповещение о погоде, в какое время тебе написать о ней?' if lang == 'ru' else
            "Let's set up a weather alert, what time do you want to report it?"
        )
        await state.set_state('weather_on')
    else:
        await message.answer('Не распознала :С')
