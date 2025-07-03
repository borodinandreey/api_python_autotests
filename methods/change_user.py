import requests
from data.endpoints import BASE_URL, USER_URL


class ChangeUser:

    @staticmethod
    def patch_user(data, token=None):
        headers = {"Authorization": token}
        response = requests.patch(f"{BASE_URL}{USER_URL}", json=data, headers=headers)
        return response.status_code, response.json()
