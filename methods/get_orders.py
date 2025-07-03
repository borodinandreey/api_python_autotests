import requests
from data.endpoints import BASE_URL, ORDER_URL


class GetOrders:

    @staticmethod
    def get_user_orders(token=None):
        headers = {"Authorization": token}
        response = requests.get(f"{BASE_URL}{ORDER_URL}", headers=headers)
        return response.status_code, response.json()
