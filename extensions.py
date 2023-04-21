"""Классы

    Raises:
        class APIException: Пользовательские исключения

    Returns:
        class ConvertedValute: возвращает float или False
"""
import json
import requests
from config import keys, TOKEN_API_LAYER

# Исключения
class APIException(Exception):
    pass

# ApiLayer
# Функция которая отправляет и получает данные с апи
class ConvertedValute:
    @staticmethod
    def get_price(fixer_to: str, fixer_from: str, amount: float)-> float:

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f"Не удалось обработать количество {amount}")

        try:
            key_fixer_to = keys[fixer_to]
        except KeyError:
            raise APIException(f"Не удалось обработать валюту {fixer_to}")

        try:
            key_fixer_from = keys[fixer_from]
        except KeyError:
            raise APIException(f"Не удалось обработать валюту {fixer_from}")

        if key_fixer_to ==  key_fixer_from:
            raise APIException(f"Одинаковые параметры {fixer_to} и {fixer_from}")


        payload = {}
        url = f"https://api.apilayer.com/fixer/convert?to={key_fixer_to}&from={key_fixer_from}&amount={amount}"

        headers= {
            "apikey": TOKEN_API_LAYER
        }

        response = requests.get(url, headers=headers, data = payload)

        status_code = response.status_code
        if status_code == 200:
            result_text = json.loads(response.text)
            result = result_text["result"]
            return result
        else :
            return False

    @staticmethod
    def count_values(values: list)-> None:
        '''Проверка количества параметров'''
        if len(values) > 3:
            raise APIException("Слишком много параметров")

        if len(values) < 3:
            raise APIException("Слишком мало параметров")