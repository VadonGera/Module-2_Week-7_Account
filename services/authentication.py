# TODO: Сервисы для аутентификации и авторизации пользователей
from config.settings import S_RUS, S_RUS_UPPER, PATH_ACCOUNTS_DATA, PATH_USERS_DATA
from utils.file_handler import DataBase
from string import ascii_letters
import hashlib
import random
import string
import uuid
import re


def contains_user(username: str, password: str) -> dict:
    db = DataBase(path=PATH_USERS_DATA, table='users')
    if not db.contains_field(username, 'username'):
        raise TypeError(f'В базе данных пользователь не зарегистрирован.')
    user = db.get_by_field(username, 'username')
    user['doc_id'] = user.doc_id
    if not check_password(password, user['password']):
        raise TypeError(f'Не верный пароль.')
    return user


def check_password(password, user_password: str) -> bool:
    if password is None:
        password = input("Введите пароль: ")
    hash_password, salt = user_password.split(',')
    return hash_password == hashlib.sha256(password.encode() + salt.encode()).hexdigest()


def register(username: str) -> dict:
    db = DataBase(path=PATH_USERS_DATA, table='users')
    if db.contains_field(username, 'username'):
        raise TypeError(f'В базе данных пользователь с логином "{username}" уже зарегистрирован.')
    user = {}
    fullname = varify_fullname(input('Введите ФИО: '))
    email = varify_email(input('Введите e-mail: '))
    password = varify_password(input('Придумайте пароль: '))
    user['username'] = username
    user['fullname'] = fullname
    user['email'] = email
    user['password'] = set_password(password)
    user['uuid'] = str(uuid.uuid4())
    user['doc_id'] = db.insert(user)
    return user


def set_password(password: str, salt: str = None) -> str:
    if salt is None:
        salt = make_salt()
    return hashlib.sha256(password.encode() + salt.encode()).hexdigest() + "," + salt


def make_salt() -> str:
    return ''.join(random.choice(string.ascii_letters) for _ in range(5))


def varify_email(email: str) -> str:
    match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email)
    if not match:
        raise TypeError(f'Не верный формат записи e-mail.')
    return email


def varify_fullname(fullname: str) -> str:
    if len(fullname) < 1:
        raise TypeError('В ФИО должен быть хотя бы один символ.')
    f = fullname.split()
    letters = ascii_letters + S_RUS + S_RUS_UPPER
    for s in f:
        if len(s.strip(letters)) != 0:
            raise TypeError('В ФИО можно использовать только буквенные символы и дефис.')
    return fullname


def varify_password(password: str) -> str:
    if len(password) < 3:
        raise TypeError('Пароль должен содержать быть хотя 3 символа.')
    return password


def get_accounts(user):
    db = DataBase(path=PATH_ACCOUNTS_DATA, table=user.user_uuid)
    accounts = db.get_all()
    print('============================================================')
    print(f'Счета пользователя "{user.fullname}":')
    if len(accounts) == 0:
        print(f'У пользователя нет счетов.')
    else:
        for a in accounts:
            print(f'--- Счет: {a.doc_id}, Имя: "{a["name"]}", Баланс: {a["balance"]:,.2f} {a["currency"]}')
    print('============================================================')
    return len(accounts)
