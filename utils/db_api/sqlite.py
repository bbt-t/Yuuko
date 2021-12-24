import sqlite3

from loader import logger_guru




class Database:
    def __init__(self, path_to_database='data/sql_db.db'):
        self.path_to_database = path_to_database

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_database)

    def execute(self, sql: str, parameters: tuple = tuple(), fetchone=False, fetchall=False, commit=False):
        parameters = tuple(parameters)
        connection = self.connection
        connection.set_trace_callback(self.logger)
        cursor = connection.cursor()
        cursor.execute(sql, parameters)
        data = None
        if commit:
            connection.commit()
        if fetchone:
            data = cursor.fetchone()
        if fetchall:
            data = cursor.fetchall()
        connection.close()
        return data

    @staticmethod
    def logger(statement):
        logger_guru.info(f"\n----------\nExecuting statement {statement}\n----------")

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join(f"{item} = ?" for item in parameters.keys())
        return sql, parameters.values()

    def create_table_users(self):
        sql = """
        CREATE TABLE Users
        (telegram_id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
        full_name varchar(128) NOT NULL,
        weather_notif_status varchar(5),
        todo_notif_status varchar(5),
        personal_pass varchar(32))
        """
        self.execute(sql, commit=True)


    def create_table_pass(self):
        sql = """
        CREATE TABLE Pass
        (telegram_id integer NOT NULL,
        name_pass varchar(32),
        pass_items BLOB)
        """
        self.execute(sql, commit=True)

    def check_personal_pass(self, **kwargs):
        sql = "SELECT personal_pass FROM Users WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchone=True)

    def update_personal_pass(self, telegram_id: int, personal_pass):
        sql = "UPDATE Users SET personal_pass = ? WHERE ?"
        parameters = (personal_pass, telegram_id)
        self.execute(sql, parameters=parameters, commit=True)

    def update_item_pass(self, telegram_id: int, name_pass: str, pass_items: bytes):
        sql = "UPDATE Pass SET pass_items = ? WHERE ?"
        parameters = (telegram_id, name_pass, pass_items)
        self.execute(sql, parameters=parameters, commit=True)

    def add_pass(self, telegram_id: int, name_pass: str, pass_items: bytes):
        sql = "INSERT INTO Pass VALUES (?, ?, ?)"
        parameters = (telegram_id, name_pass, pass_items)
        self.execute(sql, parameters=parameters, commit=True)

    def select_pass(self, **kwargs):
        sql = "SELECT pass_items FROM Pass WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchone=True)

    def add_user(self,
                 telegram_id: int,
                 full_name: str,
                 weather_notif_status: bool = None,
                 todo_notif_status: bool = None,
                 personal_pass: str = None):

        sql = "INSERT INTO Users (telegram_id, full_name, weather_notif_status, " \
              "todo_notif_status, personal_pass) VALUES (?, ?, ?, ?, ?)"
        parameters = (telegram_id, full_name, weather_notif_status, todo_notif_status, personal_pass)
        self.execute(sql, parameters=parameters, commit=True)

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

    def count_users(self):
        return self.execute("SELECT COUNT(*) FROM Users;", fetchone=True)

    def delete_all_users(self):
        self.execute("DELETE FROM Users WHERE True")

    def del_table(self):
        self.execute("DROP TABLE Users")
        self.execute("DROP TABLE Pass")