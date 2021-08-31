import requests
import json
from config import keys, API_KEY

class APIException(Exception):
    pass

class Converter:
    @staticmethod
    def get_price(values):
        if len(values) > 3:
            raise APIException('Неправильное количество параметров.')
        quote, base, amount = values
        if quote == base:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}.')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}')

        r = requests.get(f'http://api.exchangeratesapi.io/v1/latest?access_key={API_KEY}&base={quote_ticker}&symbols={base_ticker}')
        total_base = float(amount)*float(json.loads(r.content)["rates"][base_ticker])
        return round(total_base, 2)
