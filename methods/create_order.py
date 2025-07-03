from json import JSONDecodeError

import requests
from data.endpoints import BASE_URL, ORDER_URL


class CreateOrder:

    @staticmethod
    def post_create_order(ingredients=None, token=None):
        headers = {"Authorization": token}
        response = requests.post(f"{BASE_URL}{ORDER_URL}", json=ingredients, headers=headers)
        try:
            return response.status_code, response.json()
        except JSONDecodeError:
            return response.status_code, response.text
