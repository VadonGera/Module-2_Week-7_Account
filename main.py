from models.user import User
from models.account import Account
from utils.currency_converter import get_exchange_rates
from services.transaction_management import generate_report, generate_story
from services.account_management import amount_conversion
from utils.file_handler import log_file


def menu_login():
    while True:
        user = User()
        print('Для продолжения введите номер операции.')
        print('  1. Авторизация пользователя.')
        print('  2. Регистрация нового пользователя.')
        print('  3. Выход.')
        operation = input('Введите номер операции: ')
        if operation == '1':
            operation_name = 'Авторизация пользователя'
            print(f'\n{operation_name}.')
            username = input('Введите логин: ')
            try:
                user.login(username)
            except TypeError as s:
                print(f'{s}\n')
                continue

            print(f'{operation_name} прошла успешно.')
            menu_account(user)

        elif operation == '2':
            operation_name = 'Регистрация нового пользователя'
            print(f'\n{operation_name}.')
            username = input('Придумайте логин: ')
            try:
                user.register(username)
            except TypeError as s:
                print(f'{s}\n')
                continue

            print(f'{operation_name} прошла успешно.')

            # TODO: Создаем новый счет для нового пользователя
            account = Account(user.user_uuid)
            account.set_account('Cash', 'RUB', 0.0)
            menu_account(user)

        elif operation == '3':
            print()
            print("До свидания!")
            log_file('Выход', user.user_uuid)
            exit()
        else:
            print()
            print("Указан несуществующий номер операции. Повторите попытку.")


def menu_account(user):
    get_exchange_rates()
    while True:
        account = Account(user.user_uuid)
        print('\nДля продолжения введите номер операции.')
        print("  1. Сведения о счетах.")
        print("  2. Выбор счета.")
        print("  3. Добавить новый счет.")
        print("  4. Назад.")
        operation = input("Введите номер операции: ")
        if operation == '1':
            operation_name = 'Счета пользователя'
            print(f'\n{operation_name}.')
            user.get_accounts()

        elif operation == '2':
            operation_name = 'Выбор счета пользователя'
            print(f'\n{operation_name}.')
            try:
                count = user.get_accounts()
                if count == 0:
                    continue
                try:
                    number = int(input("Укажите номер счета для проведения операций над ним (0 - для отмены): "))
                except:
                    print(f'Ошибка при выборе счета.')
                    continue

                if number == 0:
                    continue
                account.get_account(int(number))

            except TypeError as s:
                print(f'{s}\n')
                continue

            menu_report(user, account)

        elif operation == '3':
            operation_name = 'Регистрация нового счета'
            print(f'\n{operation_name}.')
            try:
                account.set_account()
            except TypeError as s:
                print(f'{s}\n')
                continue

            menu_report(user, account)

        elif operation == '4':
            print()
            break
        else:
            print()
            print("Указан несуществующий номер операции. Повторите попытку.")


def menu_report(user, account):
    while True:
        print(f'\nОперации пользователя "{user.fullname}" со счетом "{account.account_name}".')
        print(f'Для продолжения введите номер операции.')
        print('  1. Транзакции.')
        print('  2. История.')
        print('  3. Отчет.')
        print('  4. Назад.')
        operation = input('Введите номер операции: ')
        if operation == '1':
            menu_transaction(user, account)

        elif operation == '2':
            print('\nИстория.')
            try:
                print(generate_story(account))
            except TypeError as s:
                print(f'{s}\n')
                continue

        elif operation == '3':
            print('\nОтчет.')
            try:
                print(generate_report(account))
            except TypeError as s:
                print(f'{s}\n')
                continue

        elif operation == '4':
            break
        else:
            print()
            print("Указан несуществующий номер операции. Повторите попытку.")


def menu_transaction(user, account):
    while True:
        print(f'\nТранзакции пользователя "{user.fullname}" по счету "{account.account_name}".')
        print(f'Для продолжения введите номер операции.')
        print('  1. Доход.')
        print('  2. Расход.')
        print('  3. Перевод.')
        print('  4. Назад.')
        operation = input('Введите номер операции: ')
        if operation == '1':
            print(f'\nДобавить зачисление на счет "{account.account_name}".')
            income = 0
            try:
                try:
                    income = float(input("Укажите сумму дохода: "))
                except:
                    print(f'Ошибка при выборе суммы.')

                account.add_income(income)
                print(f'Зачисление прошло успешно.')
                print(f'Баланс счета "{account.account_name}": {account.get_balance():,.2f} {account.currency}')

            except TypeError as s:
                print(f'{s}\n')
                continue

        elif operation == '2':
            print('\nДобавить списание со счета.')
            income = 0
            try:
                try:
                    income = float(input("Укажите сумму расхода: "))
                except:
                    print(f'Ошибка при выборе суммы.')

                account.add_expense(income)
                print(f'Списпние прошло успешно.')
                print(f'Баланс счета "{account.account_name}": {account.get_balance():,.2f} {account.currency}')

            except TypeError as s:
                print(f'{s}\n')
                continue

        elif operation == '3':
            print('\nДобавить перевод со счета на счет.')
            transfer = Account(user.user_uuid)
            try:
                count = user.get_accounts()
                if count == 0:
                    continue
                try:
                    number = int(input("Укажите номер счета для перевода (0 - для отмены): "))
                except:
                    print(f'Ошибка при выборе счета.')
                    continue
                try:
                    amount = float(input("Укажите сумму перевода: "))
                except:
                    print(f'Ошибка при выборе суммы.')
                    continue

                account.add_expense(amount, 'перевод')
                transfer.get_account(int(number))
                transfer.add_income(amount_conversion(amount, account.currency, transfer.currency), 'перевод')

            except TypeError as s:
                print(f'{s}\n')
                continue

        elif operation == '4':
            break
        else:
            print()
            print("Указан несуществующий номер операции. Повторите попытку.")


if __name__ == "__main__":
    print("Вас приветствует система <Horns & Hooves>!")

    menu_login()
