from collections import defaultdict
from datetime import timedelta

from config import time_now
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



