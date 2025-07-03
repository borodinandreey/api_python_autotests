import allure
import pytest
from data.messages import AUTHORIZATION_FALSE_MESSAGE
from helper.helper_user import create_fake_email, create_fake_password, create_fake_name
from methods.change_user import ChangeUser
from methods.create_user import CreateUser
from methods.login_user import LoginUser


@allure.feature("Тесты на изменение пользователя")
class TestChangeUser:

    @pytest.mark.parametrize("data", [
        {"email": create_fake_email()},
        {"name": create_fake_name()}
    ])
    @allure.title("Проверка изменения данных пользователя: email и name")
    def test_change_user_email_and_name_successful(self, user_payload, delete_user, data):
        with allure.step("Создание пользователя"):
            status_code, response_body, token = CreateUser.post_create_user(payload=user_payload)
            delete_user.append(token)
        with allure.step(f"Изменение данных пользователя: {data}"):
            status_code, response_body = ChangeUser.patch_user(data=data, token=token)
        with allure.step("Проверка, что статус код: 200"):
            assert status_code == 200
        with allure.step("Проверка, что параметр 'success': True"):
            assert response_body["success"] is True
        with allure.step(f"Проверка изменения данных пользователя: {data}"):
            for key, value in data.items():
                actual_result = response_body["user"].get(key)
                assert actual_result == value

    @allure.title("Проверка изменения данных пользователя: password")
    def test_change_user_password_successful(self, user_payload, delete_user):
        with allure.step("Создание пользователя"):
            status_code, response_body, token = CreateUser.post_create_user(payload=user_payload)
            delete_user.append(token)
        with allure.step("Запись использованных данных пользователя в переменную"):
            email = user_payload["email"]
        with allure.step("Создание нового пароля"):
            new_password = create_fake_password()
            new_password_payload = {"password": new_password}
        with allure.step(f"Изменение данных пользователя: password"):
            status_code, response_body = ChangeUser.patch_user(data=new_password_payload, token=token)
        with allure.step("Проверка, что статус код: 200"):
            assert status_code == 200
        with allure.step("Проверка, что параметр 'success': True"):
            assert response_body["success"] is True
        with allure.step("Проверка успешной авторизации с новым паролем"):
            new_payload = {
                "email": email,
                "password": new_password
            }
            status_code, response_body, token = LoginUser.post_login_user(payload=new_payload)
        with allure.step("Проверка, что статус код: 200"):
            assert status_code == 200
        with allure.step("Проверка, что параметр 'success': True"):
            assert response_body["success"] is True
        with allure.step("Проверка, что 'accessToken' присутствует в теле ответа"):
            assert "accessToken" in response_body

    @pytest.mark.parametrize("data", [
        {"email": create_fake_email()},
        {"password": create_fake_password()},
        {"name": create_fake_name()}
    ])
    @allure.title("Проверка изменения данных пользователя без токена авторизации")
    def test_change_user_data_unsuccessful(self, data):
        with allure.step(f"Изменение данных пользователя: {data}"):
            status_code, response_body = ChangeUser.patch_user(data=data)
        with allure.step("Проверка, что статус код: 401"):
            assert status_code == 401
        with allure.step("Проверка, что параметр 'success': False"):
            assert response_body["success"] is False
        with allure.step("Проверка корректности сообщения"):
            assert response_body["message"] == AUTHORIZATION_FALSE_MESSAGE
