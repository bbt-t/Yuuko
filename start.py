from aiogram.utils import executor
from sqlalchemy import exc

from loader import dp, scheduler, logger_guru
from handlers.todo_handl import save_pkl_obj, delete_all_todo
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

    logger_guru.warning('START BOT')


@logger_guru.catch()
async def on_shutdown(dp):
    """
    Notifying admins about the stop of the bot, save Todo objects.
    :param dp: Dispatcher
    """
    from utils.notify_admins import on_shutdown_notify
    await on_shutdown_notify(dp)
    await save_pkl_obj()
    await dp.storage.close()
    await dp.storage.wait_closed()
    raise SystemExit


if __name__ == '__main__':
    scheduler.start()
    try:
        executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown, skip_updates=True)
    except BaseException as err:
        logger_guru.critical(f'{repr(err)} : STOP BOT')