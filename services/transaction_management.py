# TODO: Управление транзакциями
from config.settings import PATH_TRANSACTION_DATA, FORMAT_DATE
from utils.file_handler import DataBase
import dateparser
import datetime


def add_transaction(transaction):
    db = DataBase(path=PATH_TRANSACTION_DATA, table=transaction.account_uuid)
    trans = {'uuid': transaction.transaction_uuid, 'amount': transaction.amount,
             'type': transaction.transaction_type, 'date': transaction.date, 'note': transaction.note}
    db.insert(trans)


def format_date(date_str: str, my_format: str = FORMAT_DATE) -> datetime.datetime:
    return datetime.datetime.strptime(date_str, my_format)


def set_period(start_date: str = None, end_date: str = None):
    if start_date is None:
        start_date = input('Введите начальную дату периода: ')
        start_date = dateparser.parse(start_date, languages=['en', 'ru'])
    if end_date is None:
        end_date = input('Введите конечную дату периода: ')
        end_date = dateparser.parse(end_date, languages=['en', 'ru'])

    return start_date, end_date


def get_transactions(account, start_date, end_date):
    db = DataBase(path=PATH_TRANSACTION_DATA, table=account.account_uuid)
    accounts = db.get_all()
    # start_date, end_date = set_period(start_date, end_date)
    result = list(filter(lambda trans: start_date < format_date(trans['date']) <= end_date, accounts))
    return result


def generate_report(account, start_date: str = None, end_date: str = None):
    start_date, end_date = set_period(start_date, end_date)
    transactions = get_transactions(account, start_date, end_date)
    total_income, total_expense, final_balance = 0.0, 0.0, 0.0
    for tr in transactions:
        final_balance += tr['amount'] * tr['type']
        if tr['type'] == 1:
            total_income += tr['amount']
        elif tr['type'] == -1:
            total_expense += tr['amount']

    period = (f'c {datetime.datetime.strftime(start_date, "%Y.%m.%d")} по '
              f'{datetime.datetime.strftime(end_date, "%Y.%m.%d")}')
    result = (
        f'Транзакции по счету "{account.account_name}" за период {period}:\n'
        f'--- Общий доход: {total_income:,.2f} {account.currency}\n'
        f'--- Общий расход: {total_expense:,.2f} {account.currency}\n'
        f'--- Итого за период: {final_balance:,.2f} {account.currency}'
    )

    return result


def generate_story(account, start_date: str = None, end_date: str = None):
    start_date, end_date = set_period(start_date, end_date)
    transactions = get_transactions(account, start_date, end_date)
    period = (f'c {datetime.datetime.strftime(start_date, "%Y.%m.%d")} по '
              f'{datetime.datetime.strftime(end_date, "%Y.%m.%d")}')
    result = (
        f'Транзакции по счету "{account.account_name}" за период {period}:\n')
    for tr in transactions:
        result += (f'--- Транзакция: {tr["uuid"]}, {tr["date"]}, '
                   f'{tr["type"] * tr["amount"]:,.2f} {account.currency}, {tr.get("note", "")}\n')

    return result
