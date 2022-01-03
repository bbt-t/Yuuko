from asyncio import sleep as asyncio_sleep

from aiogram import Dispatcher, types
from aiogram.dispatcher import DEFAULT_RATE_LIMIT
from aiogram.dispatcher.handler import CancelHandler, current_handler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.utils.exceptions import Throttled

from utils.stickers_info import SendStickers




def rate_limit(limit: int, key=None):
    """
    Decorator for the handler (to simplify the code)
    :param limit: timeout messages from the user
    :param key: an additional parameter, with the help of it the function distinguishes handlers from each other
    (you can catomise your own trotting parameter for a specific handler / group of handlers)
    """
    def decorator(func):
        setattr(func, 'throttling_rate_limit', limit)
        if key:
            setattr(func, 'throttling_key', key)
        return func
    return decorator


class ThrottlingMiddleware(BaseMiddleware):
    """
    Anti-flood
    """
    def __init__(self, limit=DEFAULT_RATE_LIMIT, key_prefix='antiflood_'):
        self.rate_limit = limit
        self.prefix = key_prefix
        super(ThrottlingMiddleware, self).__init__()

    async def on_process_message(self, message: types.Message | types.CallbackQuery, data: dict):
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

    async def message_throttled(self, message: types.Message | types.CallbackQuery, throttled: Throttled):
        handler = current_handler.get()
        dispatcher = Dispatcher.get_current()
        if handler:
            key = getattr(handler, 'throttling_key', f"{self.prefix}_{handler.__name__}")
        else:
            key = f"{self.prefix}_message"

        delta = throttled.rate - throttled.delta

        if throttled.exceeded_count <= 2:
            await message.reply_sticker(SendStickers.you_were_bad.value)
            await message.reply('Слишком часто пишешь!')

        await asyncio_sleep(delta)

        thr = await dispatcher.check_key(key)
        if thr.exceeded_count == throttled.exceeded_count:
            await message.answer('Всё, можно писать.')
