import sqlite3

from loader import logger_guru



def logger(statement):
    """
    Вывод в принте выполняемых команд.
    """
    logger_guru.info(f"\n----------\nExecuting statement {statement}\n----------")

class Database:
    def __init__(self, path_to_database='data/sql_db.db'):
        self.path_to_database = path_to_database

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_database)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = tuple()
        parameters = tuple(parameters)
        connection = self.connection
        connection.set_trace_callback(logger)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchone:
            data = cursor.fetchone()
        if fetchall:
            data = cursor.fetchall()
        connection.close()
        return data

    def create_table_users(self):
        sql = """
        CREATE TABLE Users
        (telegram_id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
        full_name varchar(128) NOT NULL,
        weather_notif_status varchar(5),
        todo_notif_status varchar(5))
        """
        self.execute(sql, commit=True)

    def add_user(self,
                 telegram_id: int,
                 full_name: str,
                 weather_notif_status: bool = None,
                 todo_notif_status: bool = None):

        sql = "INSERT INTO Users (telegram_id, full_name, weather_notif_status, todo_notif_status) VALUES (?,?,?,?)"
        parameters = (telegram_id, full_name, weather_notif_status, todo_notif_status)
        self.execute(sql, parameters=parameters, commit=True)

    def update_weather_status(self, telegram_id: int, weather_notif_status: bool):
        sql = "UPDATE Users SET weather_notif_status = ? WHERE ?"
        parameters = (weather_notif_status, telegram_id)
        self.execute(sql, parameters=parameters, commit=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join(f"{item} = ?" for item in parameters.keys())
        return sql, parameters.values()

    def select_all_id(self):
        sql = "SELECT telegram_id FROM Users"
        return self.execute(sql, fetchall=True)

    def select_all_user(self):
        sql = "SELECT * FROM Users"
        return self.execute(sql, fetchall=True)

    def select_user(self, **kwargs):
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchone=True)

    def select_all_users_weather(self, **kwargs):
        sql = "SELECT telegram_id, weather_notif_status FROM Users WHERE weather_notif_status IS NOT NULL"
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql,parameters=parameters, fetchall=True)

    def count_users(self):
        return self.execute("SELECT COUNT(*) FROM Users;", fetchone=True)

    def delete_all_users(self):
        self.execute("DELETE FROM Users WHERE True")

    def del_table(self):
        self.execute("DROP TABLE Users")