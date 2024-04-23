# TODO: Класс Transaction для учета транзакций
import uuid
import datetime
from services.transaction_management import add_transaction
from config.settings import FORMAT_DATE


class Transaction():

    def __init__(self, account_uuid, amount: float, transaction_type: int, note: str):
        self.transaction_uuid = None
        self.account_uuid = account_uuid
        self.amount: float = amount
        self.note = note
        self.transaction_type: int = transaction_type
        self.date = None

    def record_transaction(self):
        self.transaction_uuid = str(uuid.uuid4())
        self.date = datetime.datetime.now().strftime(FORMAT_DATE)
        add_transaction(self)
