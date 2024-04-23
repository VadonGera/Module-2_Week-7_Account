# TODO: Управление счетами пользователей
from config.settings import PATH_ACCOUNTS_DATA, PATH_EXCHANGE_DATA
from utils.file_handler import DataBase
import uuid


# TODO: Получаем данные счета из базы данных
def upload_account(account, doc_id: int):
    db = DataBase(path=PATH_ACCOUNTS_DATA, table=account.user_uuid)
    if not db.contains_id(doc_id):
        raise TypeError(f'В базе данных указанный счет отсутствует.')
    result = db.get_by_id(doc_id)
    account.account_uuid = result.get('uuid', None)
    account.account_name = result.get('name', None)
    account.currency = result.get('currency', None)
    account.balance = result.get('balance', None)
    account.account_id = result.doc_id


# TODO: Создаем новый счет для пользователя user_uuid
def create_account(account, name: str, currency: str) -> list[int]:
    if name is None:
        name = input('Введите имя нового счета: ')
    db = DataBase(path=PATH_ACCOUNTS_DATA, table=account.user_uuid)
    if db.contains_field(name, 'name'):
        raise TypeError(f'В базе данных счет с именем "{name}" уже зарегистрирован.')
    if currency is None:
        currency = input('Укажите валюту счета: ')
    currency = currency.upper()
    if not currency_in_dict(currency):
        raise TypeError(f'Не верный формат валюты.')
    account.account_uuid = str(uuid.uuid4())
    account.account_name = name
    account.currency = currency
    account.balance = 0.0
    result = update_account(account)
    return result


# TODO: Обновляем данные счета в базе данных
def update_account(account) -> list[int]:
    db = DataBase(path=PATH_ACCOUNTS_DATA, table=account.user_uuid)
    my_account = {'name': account.account_name, 'currency': account.currency,
                  'balance': account.balance, 'uuid': account.account_uuid}
    result = db.upsert(account.account_uuid, 'uuid', my_account)
    return result


def balance_account(account):
    print(f'Баланс счета "{account.account_name}": {account.get_balance():,.2f} {account.currency}')


# TODO: Проверяем код валюты
def currency_in_dict(currency):
    db = DataBase(path=PATH_EXCHANGE_DATA, table='rates')
    rates = db.get_by_id(1)
    return currency in rates


# TODO: Конвертация из одной валюты в другую
def amount_conversion(amount: float, currency_of: str, currency_in: str):
    db = DataBase(path=PATH_EXCHANGE_DATA, table='rates')
    rates = db.get_by_id(1)
    rate_of = rates[currency_of]
    rate_in = rates[currency_in]

    return amount * rate_in / rate_of
