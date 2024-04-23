from services.account_management import *


def test_currency_in_dict():
    assert currency_in_dict("RUB") == True
    assert currency_in_dict("RUwwwB") == False
