from aiogram.types import Message, ContentType
from aiogram.dispatcher.filters.builtin import Command
from aiogram.dispatcher import FSMContext
from aiohttp import ClientSession
from ujson import dumps as ujson_dumps

from config import work_with_api
from loader import dp




@dp.message_handler(Command('show_text'))
async def start_weather(message: Message, state: FSMContext):
    text_msg: str = ('Привет! я могу попробовать прочитать что написано, '
               'отправь мне фото, чем "лучше" (качествнней) оно будет, тем точнее я дам ответ...')

    await message.answer(text_msg)
    await message.answer('<s>ТСС! это пока что находится в стадии тестирования!</s>')
    await state.set_state('send_image')


@dp.message_handler(state='send_image', content_types=ContentType.PHOTO)
async def take_image_for_ocr(message: Message, state: FSMContext):
    data = ujson_dumps({'imageurl': f'{await message.photo[-1].get_url()}'})
    headers: dict = {'Content-Type': 'application/json', 'accept': 'application/json'}

    async with ClientSession() as session:
        async with session.post(url=work_with_api['OTHER']['OCR_URL'], headers=headers, data=data) as resp:
            result: str = '\n'.join(await resp.text())

    if result:
        await message.answer(f'Вот что получилось:\n{result}')
    else:
        await message.answer('Что-то не так :( не могу прочитать ...')

    await state.finish()
