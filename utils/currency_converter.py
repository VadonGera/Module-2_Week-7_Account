import requests
from utils.file_handler import DataBase
from config.settings import PATH_EXCHANGE_DATA


# TODO: Утилита для получения курсов валют
def get_exchange_rates(currency='RUB'):
    # API endpoint для получения курсов валют
    url = f"https://api.exchangerate-api.com/v4/latest/{currency}"
    # Отправляем GET-запрос для получения данных
    response = requests.get(url)
    # Проверяем успешность запроса
    if response.status_code == 200:
        # Получаем курс обмена из данных
        data = response.json()
        # Сохраняем полученные данные
        db_rates = DataBase(path=PATH_EXCHANGE_DATA, table='rates')
        db_rates.delete('rates')
        db_rates.insert(data['rates'])
    else:
        raise TypeError('Ошибка при получении данных.')
