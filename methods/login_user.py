import requests
from data.endpoints import BASE_URL, LOGIN_USER_URL


class LoginUser:

    @staticmethod
    def post_login_user(payload=None):
        response = requests.post(f"{BASE_URL}{LOGIN_USER_URL}", json=payload)
        json_response = response.json()

        access_token = json_response.get("accessToken")

        return response.status_code, json_response, access_token
