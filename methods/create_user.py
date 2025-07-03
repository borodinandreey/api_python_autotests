import requests
from data.endpoints import BASE_URL, CREATE_USER_URL, USER_URL


class CreateUser:

    @staticmethod
    def post_create_user(payload=None):
        response = requests.post(f"{BASE_URL}{CREATE_USER_URL}", json=payload)
        json_response = response.json()

        access_token = json_response.get("accessToken")

        return response.status_code, json_response, access_token

    @staticmethod
    def delete_create_user(token):
        headers = {"Authorization": token}
        response = requests.delete(f"{BASE_URL}{USER_URL}", headers=headers)
        return response.status_code, response.json()
