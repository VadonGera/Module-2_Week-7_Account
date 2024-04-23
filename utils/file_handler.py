# TODO: Утилиты для работы с файлами (чтение, запись)
from tinydb import TinyDB, Query, where
from config.settings import PATH_LOG_DATA
import datetime


# TODO: Утилита для фиксации логов
def log_file(operation, user_uuid, note: str = None):
    with open(PATH_LOG_DATA, 'a', encoding='utf-8') as file_log:
        s = f'[{datetime.datetime.now()}] [{user_uuid}] [{operation}]'
        if note is not None:
            s = f'{s} [{note}]'
        file_log.write(s + '\n')


# TODO: Класс DataBase для работы с json
class DataBase:

    def __init__(self, path, table):
        self.__db = TinyDB(path)
        self.__table = self.__db.table(table)
        self.__Search = Query()

    def contains_field(self, *args) -> bool:
        result = self.__table.contains(where(args[1]) == args[0])
        return result

    def contains_id(self, *args) -> bool:
        result = self.__table.contains(doc_id=args[0])
        return result

    def update(self, *args):
        self.__table.update({args[1]: args[2]}, doc_ids=[args[0]])
        # return result

    def get_by_id(self, *args):  # Document()
        result = self.__table.get(doc_id=args[0])
        return result

    def get_by_field(self, *args):  # Document()
        result = self.__table.get(where(args[1]) == args[0])
        return result

    def insert(self, *args) -> int:
        result = self.__table.insert(args[0])
        return result

    # TODO: args[2] - {dict}, args[1] - search field, args[0] - search value, return - list[doc_id, doc_id, doc_id]
    def upsert(self, *args) -> list[int]:
        result = self.__table.upsert(args[2], where(args[1]) == args[0])
        return result

    def get_all(self):
        return self.__table.all()

    def delete(self, *args):
        self.__db.drop_table(args[0])
