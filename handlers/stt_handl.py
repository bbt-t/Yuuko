from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ContentType

from config import FOLDER_ID, API_YA_STT
from loader import dp
from utils.notify_users import send_weather
from utils.work_with_speech.speech_to_text_yandex import recognize_speech_by_Ya




@dp.message_handler(content_types=ContentType.VOICE)
async def determine_further_path(message: Message, state: FSMContext):
    file_url: str = await message.voice.get_url()
    text: str = recognize_speech_by_Ya(file_url, FOLDER_ID, API_YA_STT)

    if any(let.lower().startswith('пого') for let in text.split()):
        await message.answer('Давай настроем оповещение о погоде, в какое время тебе напомнать оней?')
        await send_weather(message.from_user.id)
        await state.set_state('weather_on')
    else:
        await message.answer('Не распознала :С')

