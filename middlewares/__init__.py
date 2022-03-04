from aiogram import Dispatcher
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from .throttling import ThrottlingMiddleware
from .validate_users import ValidateMessage


def setup(dp: Dispatcher):
    dp.setup_middleware(ThrottlingMiddleware())
    dp.setup_middleware(LoggingMiddleware())
    dp.setup_middleware(ValidateMessage())

