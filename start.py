from typing import Literal, final

from aiogram import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.executor import start_webhook, start_polling
from click import command, option
from sqlalchemy import exc

from config import hook_info
from loader import dp, scheduler, logger_guru
from tests.schemas.pydantic_schemas import WebHook
from utils.database_manage.redis.clear_redis_data import clear_redis
from utils.database_manage.sql.sql_commands import start_db
from utils.misc.notify_admins import on_startup_notify, on_shutdown_notify
from utils.misc.other_funcs import clear_all_pin_msg
from utils.misc.set_bot_commands import set_default_commands
from utils.todo import delete_all_todo

import handlers
from middlewares import setup


@final
class StartBotCompose:
    webhook: bool = False

    @classmethod
    async def on_startup(cls, dp: Dispatcher):
        """
        Registration of handlers, middlewares, notifying admins about the start of the bot,
        an attempt to create a table User if it does not exist.
        :param dp: Dispatcher
        """
        if cls.webhook:
            await dp.bot.set_webhook(hook_info.get('WEBHOOK_URL'), drop_pending_updates=True)
        setup(dp)
        await set_default_commands(dp)
        await on_startup_notify(dp)
        try:
            await start_db()
        except exc:
            logger_guru.info('DB error on start bot')
        scheduler.start()
        for func in {delete_all_todo, clear_redis, clear_all_pin_msg}:
            scheduler.add_job(func, 'cron', id=f'{func}_job',
                              day_of_week='mon-sun', hour='00', minute='01', end_date='2023-05-30',
                              misfire_grace_time=5, replace_existing=True, timezone="Europe/Moscow")
        logger_guru.warning('Bot is running')

    async def on_shutdown(dp: Dispatcher):
        """
        Notifying admins about the stop of the bot, save Todo objects.
        :param dp: Dispatcher
        """
        await on_shutdown_notify(dp)
        await dp.bot.delete_webhook(drop_pending_updates=True)
        await dp.storage.close()
        await dp.storage.wait_closed()
        raise SystemExit


@command()
@option("--storage", default=None, help="Method used (or mem or redis (default))")
@option("--method", default=None, help="Connection method used or polling (default) or webhook")
def _start_bot(storage: Literal['mem', 'redis', None], method: Literal['webhook', None]) -> None:
    """
    CLI.
    :param storage: Using the "mem" flag will break some bot functionality
    :param method: connection method used
    """
    if storage == 'mem':
        dp.__setattr__('storage', MemoryStorage())
    try:
        if method == 'webhook' and WebHook.parse_obj(hook_info):
            logger_guru.warning('---> With webhook --->')
            setattr(StartBotCompose, 'webhook', True)
            start_webhook(
                dispatcher=dp,
                skip_updates=True,
                on_startup=StartBotCompose.on_startup,
                on_shutdown=StartBotCompose.on_shutdown,
                **hook_info.get('WEBHOOK')
            )
        else:
            logger_guru.warning('---> With polling --->')
            start_polling(
                dispatcher=dp,
                on_startup=StartBotCompose.on_startup,
                on_shutdown=StartBotCompose.on_shutdown,
                skip_updates=True
            )
    except BaseException as err:
        logger_guru.critical(f'{repr(err)} : Bot stopped')


if __name__ == '__main__':
    _start_bot()
