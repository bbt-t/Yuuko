from asyncio import set_event_loop_policy as asyncio_set_event_loop_policy

from aiogram.utils.executor import start_webhook
from uvloop import EventLoopPolicy as uvloop_Loop
from sqlalchemy import exc

from config import WEBHOOK_URL, WEBHOOK_PATH, WEBAPP_HOST, WEBAPP_PORT
from loader import dp, scheduler, logger_guru, bot
from handlers.todo_handl import save_pkl_obj, delete_all_todo
from utils.clear_redis_data import clear_redis
from utils.db_api.sql_commands import start_db
from utils.notify_users import send_todo_voice_by_ya




async def on_startup(dp):
    """
    Registration of handlers, middlewares, notifying admins about the start of the bot,
    an attempt to create a table User if it does not exist.
    :param dp: Dispatcher
    """
    import middlewares
    import handlers
    import filters
    await bot.delete_webhook()
    await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)
    from utils.set_bot_commands import set_default_commands
    await set_default_commands(dp)
    from utils.notify_admins import on_startup_notify
    await on_startup_notify(dp)
    try:
        await start_db()
    except exc:
        logger_guru.info('DB error on start bot')

    scheduler.add_job(send_todo_voice_by_ya, 'cron', id='todo_send_msg',
                      day_of_week='mon-sun', hour='7', minute='00', end_date='2023-05-30',
                      misfire_grace_time=10, replace_existing=True, timezone="Europe/Moscow")
    scheduler.add_job(delete_all_todo, 'cron', id='todo_delete',
                      day_of_week='mon-sun', hour='23', minute='30', end_date='2023-05-30',
                      misfire_grace_time=10, replace_existing=True, timezone="Europe/Moscow")
    scheduler.add_job(clear_redis, 'cron', id='redis_delete_keys',
                      day_of_week='mon-sun', hour='00', minute='00', end_date='2023-05-30',
                      misfire_grace_time=10, replace_existing=True, timezone="Europe/Moscow")

    logger_guru.warning('START BOT')


@logger_guru.catch()
async def on_shutdown(dp):
    """
    Notifying admins about the stop of the bot, save Todo objects.
    :param dp: Dispatcher
    """
    await bot.delete_webhook()
    from utils.notify_admins import on_shutdown_notify
    await on_shutdown_notify(dp)
    await save_pkl_obj()
    await dp.storage.close()
    await dp.storage.wait_closed()
    raise SystemExit


if __name__ == '__main__':
    asyncio_set_event_loop_policy(uvloop_Loop())
    scheduler.start()
    try:
        start_webhook(
            dispatcher=dp,
            webhook_path=WEBHOOK_PATH,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            skip_updates=True,
            host=WEBAPP_HOST,
            port=WEBAPP_PORT)
    except BaseException as err:
        logger_guru.critical(f'{repr(err)} : STOP BOT')
