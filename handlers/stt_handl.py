from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ContentType

from config import FOLDER_ID, API_YA_STT
from loader import dp, logger_guru
from utils.notify_users import send_weather
from utils.work_with_speech.speech_to_text_on_their_own import recognize_locally
from utils.work_with_speech.speech_to_text_yandex import recognize_speech_by_ya




@dp.message_handler(content_types=ContentType.VOICE)
async def determine_further_path(message: Message, state: FSMContext):
    file_id: str = message.voice.file_id
    try:
        msg: bytes = await message.bot.download_file_by_id(file_id)
        text: str = recognize_speech_by_ya(msg, FOLDER_ID, API_YA_STT)
    except:
        logger_guru.error(f'{message.from_user.id} : unsuccessful request STT YANDEX!')

        name_file: str = f"{file_id}.ogg"
        file_path = (await message.bot.get_file(file_id)).file_path
        await message.bot.download_file(file_path, name_file)
        text: str = recognize_locally(name_file)

    if any(let.lower().startswith('пого') for let in text.split()):
        await message.answer('Давай настроем оповещение о погоде, в какое время тебе написать о ней?')
        await send_weather(message.from_user.id)
        await state.set_state('weather_on')
    else:
        await message.answer('Не распознала :С')