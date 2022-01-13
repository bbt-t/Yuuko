from aiogram import Dispatcher
from aiogram.utils.executor import start_webhook
from sqlalchemy import exc

from config import WEBHOOK_URL, WEBHOOK_PATH, WEBAPP_HOST, WEBAPP_PORT
from loader import dp, scheduler, logger_guru, bot
from utils.clear_redis_data import clear_redis
from utils.db_api.sql_commands import start_db
from utils.todo import delete_all_todo




async def on_startup(dp: Dispatcher):
    """
    Registration of handlers, middlewares, notifying admins about the start of the bot,
    an attempt to create a table User if it does not exist.
    :param dp: Dispatcher
    """
    import middlewares
    import handlers
    from utils.set_bot_commands import set_default_commands
    from utils.notify_admins import on_startup_notify

    await bot.delete_webhook()
    await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)

    await set_default_commands(dp)
    await on_startup_notify(dp)

    try:
        await start_db()
    except exc:
        logger_guru.info('DB error on start bot')

    scheduler.start()
    scheduler.add_job(delete_all_todo, 'cron', id='todo_delete',
                      day_of_week='mon-sun', hour='00', minute='01', end_date='2023-05-30',
                      misfire_grace_time=5, replace_existing=True, timezone="Europe/Moscow")
    scheduler.add_job(clear_redis, 'cron', id='redis_delete_keys',
                      day_of_week='mon-sun', hour='00', minute='01', end_date='2023-05-30',
                      misfire_grace_time=5, replace_existing=True, timezone="Europe/Moscow")

    logger_guru.warning('START BOT')


@logger_guru.catch()
async def on_shutdown(dp: Dispatcher):
    """
    Notifying admins about the stop of the bot, save Todo objects.
    :param dp: Dispatcher
    """
    from utils.notify_admins import on_shutdown_notify
    await on_shutdown_notify(dp)
    await dp.storage.close()
    await dp.storage.wait_closed()
    raise SystemExit


if __name__ == '__main__':
    try:
        start_webhook(
            dispatcher=dp, skip_updates=True,
            on_startup=on_startup, on_shutdown=on_shutdown,
            webhook_path=WEBHOOK_PATH, host=WEBAPP_HOST, port=WEBAPP_PORT
        )
    except BaseException as err:
        logger_guru.critical(f'{repr(err)} : STOP BOT')
