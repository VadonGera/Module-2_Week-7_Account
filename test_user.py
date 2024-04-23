from models.user import *
from services.authentication import *


def test_user_login():
    user = User()
    user.login('poi', 'poi')
    assert user.fullname == "Points"


def test_varify_fullname():
    assert varify_fullname('user') == "user"


def test_varify_password():
    assert varify_password('user') == "user"


def test_varify_email():
    assert varify_email('user@asd.ru') == "user@asd.ru"
