# TODO: Класс User для учета пользователей
from services.authentication import register, get_accounts, contains_user
from utils.file_handler import log_file


class User:

    def __init__(self):
        self._user_uuid = None
        self._username = None
        self._fullname = None
        self._email = None
        self._password = None
        self._user_id = None

    def login(self, username: str, password: str = None) -> None:
        user = contains_user(username, password)
        self._user_uuid = user.get('uuid', None)
        self._username = user.get('username', username)
        self._fullname = user.get('fullname', None)
        self._email = user.get('email', None)
        self._password = user.get('password', None)
        self._user_id = user.get('doc_id', None)
        log_file('Авторизация пользователя', self._user_uuid)

    def register(self, username: str) -> None:
        user = register(username)
        self._user_uuid = user.get('uuid', None)
        self._username = user.get('username', username)
        self._fullname = user.get('fullname', None)
        self._email = user.get('email', None)
        self._password = user.get('password', None)
        self._user_id = user.get('doc_id', None)
        log_file('Регистрация нового пользователя', self._user_uuid)

    def get_accounts(self):
        if self._user_uuid is None:
            raise TypeError(f'Для получения доступа к счетам необходимо пройти авторизацию.')
        return get_accounts(self)

    @property
    def user_uuid(self):
        return self._user_uuid

    @property
    def fullname(self):
        return self._fullname

    @property
    def email(self):
        return self._email
