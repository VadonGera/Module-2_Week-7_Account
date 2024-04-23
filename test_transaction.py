from models.transaction import *
from utils.file_handler import DataBase
from config.settings import PATH_TRANSACTION_DATA


def test_record_transaction():
    test_account = 'test_account'
    test_note = 'test_note'
    tr = Transaction(test_account, 200, 1, 'test_note')
    tr.record_transaction()
    db = DataBase(path=PATH_TRANSACTION_DATA, table=test_account)

    assert db.contains_field(test_note, 'note') == True
    assert db.contains_field('asdasdasdasdasdasdasd', 'note') == False
    db.delete(test_account)
