from asyncio import sleep as asyncio_sleep
from typing import TypeVar, Optional, Callable

from aiogram import Dispatcher, types
from aiogram.dispatcher import DEFAULT_RATE_LIMIT
from aiogram.dispatcher.handler import CancelHandler, current_handler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.utils.exceptions import Throttled

from utils.database_manage.sql.sql_commands import DB_USERS

F = TypeVar("F", bound=Callable)


def rate_limit(limit: int, key: Optional[str] = None) -> Callable[[F], F]:
    """
    Decorator for the handler (to simplify the code)
    :param limit: timeout messages from the user
    :param key: an additional parameter, with the help of it the function distinguishes handlers from each other
    (you can catomise your own trotting parameter for a specific handler / group of handlers)
    """
    def decorator(func) -> F:
        setattr(func, 'throttling_rate_limit', limit)
        if key:
            setattr(func, 'throttling_key', key)
        return func
    return decorator


class ThrottlingMiddleware(BaseMiddleware):
    """
    Anti-flood
    """
    def __init__(self, limit: int = DEFAULT_RATE_LIMIT, key_prefix: str = 'antiflood_') -> None:
        self.rate_limit = limit
        self.prefix = key_prefix
        super(ThrottlingMiddleware, self).__init__()

    async def on_process_message(self, message: types.Message | types.CallbackQuery, data: dict) -> None:
        handler, dpr = current_handler.get(), Dispatcher.get_current()
        if handler:
            limit: int = getattr(handler, 'throttling_rate_limit', self.rate_limit)
            key: str = getattr(handler, 'throttling_key', f"{self.prefix}_{handler.__name__}")
        else:
            limit, key = self.rate_limit, f"{self.prefix}_message"
        try:
            await dpr.throttle(key, rate=limit)
        except Throttled as trot:
            await self.message_throttled(message, trot)
            raise CancelHandler()

    async def message_throttled(self, message: types.Message | types.CallbackQuery, throttled: Throttled) -> None:
        handler, dispatcher = current_handler.get(), Dispatcher.get_current()
        if handler:
            key: str = getattr(handler, 'throttling_key', f"{self.prefix}_{handler.__name__}")
        else:
            key: str = f"{self.prefix}_message"
        delta: int = throttled.rate - throttled.delta
        lang, skin = await DB_USERS.select_lang_and_skin(telegram_id=message.from_user.id)
        if throttled.exceeded_count <= 2:
            await message.reply_sticker(skin.you_were_bad.value)
            await message.reply(
                'Слишком часто пишешь! флуд это плохо! 💢' if lang == 'ru' else
                'You write too often! flood is BAD! 💢'
            )
        await asyncio_sleep(delta)
        thr: Throttled = await dispatcher.check_key(key)
        if thr.exceeded_count == throttled.exceeded_count:
            await message.answer(
                'Всё, можно писать.' if lang == 'ru' else
                'Now you can write to me.'
            )
