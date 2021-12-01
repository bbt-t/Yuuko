from aiogram.dispatcher.filters import ForwardedMessageFilter
from aiogram.types import Message

from loader import dp




@dp.message_handler(is_forwarded=True)
@dp.message_handler(ForwardedMessageFilter(True))
async def forwarded_example(msg: Message):
    await msg.answer('АЙ АЙ АЙ !\nя же вижу, что это не твоё сообщение !')