# TODO: Класс Account для учета счетов пользователей
from services.account_management import *
from models.transaction import Transaction
from utils.file_handler import log_file


class Account:

    def __init__(self, user_uuid):
        self.user_uuid = user_uuid
        self.account_uuid = None
        self.account_id = None
        self.account_name = None
        self.currency = None
        self.balance: float = 0

    def get_account(self, doc_id: int):
        upload_account(self, doc_id)

    def set_account(self, name: str = None, currency: str = None, balance: float = None):
        create_account(self, name, currency)
        print(f'Счет "{self.account_name}" создан.')
        log_file('Создание счета',
                 self.user_uuid,
                 f'Имя: {self.account_name}, Валюта: {self.currency}')
        if balance is None:
            try:
                balance = float(input('Укажите начальный баланс счета: '))
            except TypeError:
                raise TypeError(f'Ошибка при вводе баланс счета.')
        self.add_income(balance)

    def add_income(self, amount: float, note: str = None):
        if amount > 0:
            self.balance += amount
            if note is None:
                note = str(input('Укажите сведения о доходе: '))
            trans = Transaction(self.account_uuid, amount, 1, note)
            trans.record_transaction()
            log_file('Пополнение счета',
                     self.user_uuid,
                     f'Имя: {self.account_name}, Сумма: {amount:,.2f} {self.currency}, Сведения: {note}')
            update_account(self)

    def add_expense(self, amount: float, note: str = None):
        if amount > 0:
            if self.balance - amount < 0:
                raise TypeError(f'Отказ. Не достаточно средств на счете.')
            self.balance -= amount
            if note is None:
                note = str(input('Укажите сведения о расходе: '))
            trans = Transaction(self.account_uuid, amount, -1, note)
            trans.record_transaction()
            log_file('Списание со счета',
                     self.user_uuid,
                     f'Имя: {self.account_name}, Сумма: {amount:,.2f} {self.currency}, Сведения: {note}')
            update_account(self)

    def get_balance(self):
        return self.balance
