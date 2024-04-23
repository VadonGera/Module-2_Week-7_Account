from utils.file_handler import *
from config.settings import *


def test_contains_field():
    db = DataBase(path=PATH_USERS_DATA, table='users')
    assert db.contains_field('poi', 'username') == True
    assert db.contains_field('poeeei', 'username') == False


def test_contains_id():
    db = DataBase(path=PATH_ACCOUNTS_DATA, table='12bc8659-7bc1-4e75-b765-13a13c9c42d7')
    assert db.contains_id(1) == True
    assert db.contains_id(199) == False
