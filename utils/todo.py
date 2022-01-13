from collections import defaultdict
from contextlib import suppress
from datetime import timedelta
from pickle import loads, PicklingError, UnpicklingError, dumps
from pickletools import optimize as pickletools_optimize

import hmac

from aiofiles import open as aiofiles_open

from config import time_now, pkl_key
from loader import logger_guru




class ToDo:
    """
    ======================
      'To-do' list class
    ======================

    | class_object + 'task', время в формате г:м:д (опционально) -> добавит 'дело' в список дел на следующий день; |
    | class_object - 'task', время в формате г:м:д (опционально) -> удалить 'дело' из тукущего для;                |                                                       |
    | вызов class_object -> вывод списка дел на текущий день                                                       |
    | class_object.transfer_next_day -> перенос списка на следующий день                                           |
    """
    __slots__ = 'id', 'todo'

    def __init__(self, id: int):
        self.id = id
        self.todo = defaultdict(list)

    def __add__(self, dispositions: list, time_todo: str):
        self.todo[time_todo].extend(dispositions)

    def __sub__(self, dispositions: str, time_todo: str = None):
        if not time_todo:
            time_todo = time_now.date()
        if self.todo.get(time_todo):
            try:
                self.todo[time_todo].remove(dispositions)
                return 'OK ! сделано.'
            except Exception as err:
                logger_guru.warning(f"{repr(err)} : ОШИБКА УДАЛЕНИЯ")
                return "Не правильно указано 'дело' !"
        else:
            return 'дата не найдена !'

    def transfer_next_day_method(self):
        try:
            date_key = time_now
            self.todo[str((date_key + timedelta(days=1)).date())].extend(self.todo[str(date_key.date())])
        except Exception as err:
            logger_guru.warning(f"{repr(err)} : ОШИБКА ПЕРЕНОСА")


async def dump_todo_obj(todo_obj: dict) -> None:
    """
    Save todo_obj to pickle-file.
    :param todo_obj: all_todo
    """
    data = pickletools_optimize(dumps(todo_obj))
    digest = hmac.digest(pkl_key.encode(), data, 'sha256')
    try:
        async with aiofiles_open('data/data_todo.pickle', mode='wb') as f:
            for items in (digest, b'delimiter', data):
                await f.write(items)
    except PicklingError as err:
        logger_guru.error(f'{repr(err)} : Error write pickle !')
    else:
        logger_guru.info('Save pkl object')


async def load_todo_obj() -> dict:
    """
    Read ToDo_object.
    """
    try:
        async with aiofiles_open('data/data_todo.pickle', mode='rb') as f:
            data = await f.read()
            digest, new_data = data.split(b'delimiter')
            digest_new: bytes = hmac.digest(pkl_key.encode(), new_data, 'sha256')
            if not hmac.compare_digest(digest_new, digest):
                raise UnpicklingError
    except PicklingError as e:
        logger_guru.critical(f'{repr(e)} : Error read pkl object !')
    else:
        logger_guru.info('pkl signatures match !')
        read_obj: dict = loads(new_data)
        return read_obj


async def delete_all_todo() -> None:
    date = (time_now - timedelta(days=1)).date()
    todo_obj: dict = await load_todo_obj()

    for item in todo_obj.values():
        with suppress(RuntimeError):
            for key in item.todo:
                if key == str(date):
                    del item.todo[key]
    await dump_todo_obj(todo_obj)