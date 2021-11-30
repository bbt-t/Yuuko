from collections import defaultdict
from dataclasses import dataclass
from datetime import timedelta
from typing import Union

from config import time_now
from loader import logger_guru
import handlers.todo_handl as todo_handl




class ToDo:
    """
    ======================
      Класс 'список дел'
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
            print(f"{repr(err)} : ОШИБКА ПЕРЕНОСА")


def todo_to_next_day():
    try:
        if todo_handl.all_todo_obj.values():
            for val in todo_handl.all_todo_obj.values():
                val.transfer_next_day_method
            else:
                logger_guru.info('----------- ALL TRANSFER_NEXT_DAY COMPLETE -----------')
    except Exception as err:
        logger_guru.error(f'{repr(err)} : TRANSFER NEXT DAY ERROR !')


@dataclass
class ShoppingList:
    """
    ==========================
    Датакласс 'список покупок'
    ==========================
    Первое добавление списком (list).
    (!) Строкой (опционально!) через зяпяту, использовать методы строки! (!)
    """
    __slots__ = 'what'
    what: Union[str, list]

    def __str__(self):
        if not isinstance(self.what, list):
            self.what: list = self.what.split(',')
        return '\n'.join(f"{i}) {val}" for i, val in enumerate(self.what, 1))





