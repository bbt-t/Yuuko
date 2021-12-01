from typing import Union
import asyncio

from aiogram import Dispatcher, types
from aiogram.dispatcher import DEFAULT_RATE_LIMIT
from aiogram.dispatcher.handler import CancelHandler, current_handler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.utils.exceptions import Throttled

def rate_limit(limit: int, key=None):
    """
    Декоратор для хендлера (для упрощения кода)
    :param limit: таймаут сообщений от пользователя
    :param key: дополнительный параметр, с помощью него функция отличает хендлерыдруг от друга
    (можно катомизировать под определённый хендлер/группу хендлеров свой параметр тротлинга)
    """
    def decorator(func):
        setattr(func, 'throttling_rate_limit', limit)
        if key:
            setattr(func, 'throttling_key', key)
        return func
    return decorator


class ThrottlingMiddleware(BaseMiddleware):

    def __init__(self, limit=DEFAULT_RATE_LIMIT, key_prefix='antiflood_'):
        self.rate_limit = limit
        self.prefix = key_prefix
        super(ThrottlingMiddleware, self).__init__()

    async def on_process_message(self, message: Union[types.Message, types.CallbackQuery], data: dict):
        handler = current_handler.get()
        dpr = Dispatcher.get_current()
        if handler:
            limit = getattr(handler, 'throttling_rate_limit', self.rate_limit)
            key = getattr(handler, 'throttling_key', f"{self.prefix}_{handler.__name__}")
        else:
            limit = self.rate_limit
            key = f"{self.prefix}_message"
        try:
            await dpr.throttle(key, rate=limit)
        except Throttled as trot:
            await self.message_throttled(message, trot)
            raise CancelHandler()

    async def message_throttled(self, message: Union[types.Message, types.CallbackQuery], throttled: Throttled):
        handler = current_handler.get()
        dispatcher = Dispatcher.get_current()
        if handler:
            key = getattr(handler, 'throttling_key', f"{self.prefix}_{handler.__name__}")
        else:
            key = f"{self.prefix}_message"

        delta = throttled.rate - throttled.delta

        if throttled.exceeded_count <= 2:
            await message.reply_sticker('CAACAgIAAxkBAAEDZZhhp4W7R60LkP0BQaSR3B-agVBpswACpAEAAhAabSIYtWa5P_cfjSIE')
            await message.reply('Слишком часто пишешь!')

        await asyncio.sleep(delta)

        thr = await dispatcher.check_key(key)
        if thr.exceeded_count == throttled.exceeded_count:
            await message.reply('Всё, можно писать.')
