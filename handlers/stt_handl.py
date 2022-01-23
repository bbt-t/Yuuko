from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ContentType

from config import FOLDER_ID, API_YA_STT
from loader import dp, logger_guru, cpu_bound_run_func
from middlewares.throttling import rate_limit
from utils.work_with_speech.speech_to_text_on_their_own import recognize_locally
from utils.work_with_speech.speech_to_text_yandex import recognize_speech_by_ya




@rate_limit(5)
@dp.message_handler(content_types=ContentType.VOICE)
async def determine_further_path(message: Message, state: FSMContext):
    file_id: str = message.voice.file_id
    try:
        msg: bytes = await message.bot.download_file_by_id(file_id)
        text: str = await recognize_speech_by_ya(msg, FOLDER_ID, API_YA_STT)
        if not text:
            raise AttributeError('BAD REQUEST')
    except:
        logger_guru.error(f'{message.from_user.id} : unsuccessful request STT YANDEX!')

        name_file: str = f"{file_id}.ogg"
        file_path = (await message.bot.get_file(file_id)).file_path
        await message.bot.download_file(file_path, name_file)
        text: str = await cpu_bound_run_func(recognize_locally, name_file)

    if any(let.lower().startswith('пого') for let in text.split()):
        await message.answer('Давай настроем оповещение о погоде, в какое время тебе написать о ней?')
        await state.set_state('weather_on')
    else:
        await message.answer('Не распознала :С')
