from aiogram.contrib.middlewares.logging import LoggingMiddleware

from loader import dp
from .throttling import ThrottlingMiddleware


if __name__ == 'middlewares':
    dp.middleware.setup(ThrottlingMiddleware())
    dp.middleware.setup(LoggingMiddleware())
