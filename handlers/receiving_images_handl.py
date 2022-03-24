from asyncio import wait_for, TimeoutError
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import Command
from aiogram.types import Message, ContentType
from ujson import dumps as ujson_dumps

from config import bot_config
from loader import dp, logger_guru
from middlewares.throttling import rate_limit
from utils.misc.other_funcs import get_image_text


@rate_limit(5, key='show_text')
@dp.message_handler(Command('show_text'))
async def start_weather(message: Message, state: FSMContext) -> None:
    text_msg: str = ('Привет! я могу попробовать прочитать что написано, '
                     'отправь мне фото, чем "лучше" (качественней) оно будет, тем точнее я дам ответ...')

    await message.answer(text_msg)
    await message.answer('<s>ТСС! это пока что находится в стадии тестирования!</s>')
    await state.set_state('send_image')


@dp.message_handler(state='send_image', content_types=ContentType.PHOTO)
async def take_image_for_ocr(message: Message, state: FSMContext) -> None:
    data = ujson_dumps({'imageurl': f'{await message.photo[-1].get_url()}'})
    headers: dict = {
        'Content-Type': 'application/json',
        'accept': 'application/json'
    }
    try:
        result: str = await wait_for(get_image_text(
            url=bot_config.work_with_api.other.OCR_URL, headers=headers, data=data),
            timeout=10
        )
        await message.answer(f'Вот что получилось:\n{result}')
    except TimeoutError as err:
        logger_guru.warning(f'{repr(err)} : request ocr timeout.')
        await message.answer('Что-то не так 🤬 не могу прочитать ...')
    finally:
        await state.finish()
