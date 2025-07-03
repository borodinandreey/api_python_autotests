import pytest
import allure
from data.messages import REQUIRED_FIELDS_MESSAGE, IS_ALREADY_EXIST_MESSAGE
from helper.helper_user import create_fake_password, create_fake_name, create_fake_email
from methods.create_user import CreateUser

@allure.feature("Тесты на создание пользователя")
class TestCreateUser:

    @allure.title("Проверка успешного создания пользователя")
    def test_create_user_successful(self, user_payload, delete_user):
        with allure.step("Создание пользователя"):
            status_code, response_body, token = CreateUser.post_create_user(payload=user_payload)
            delete_user.append(token)
        with allure.step("Проверка, что статус код: 200"):
            assert status_code == 200
        with allure.step("Проверка, что параметр 'success': True"):
            assert response_body["success"] is True
        with allure.step("Проверка, что 'accessToken' присутствует в теле ответа"):
            assert "accessToken" in response_body

    @allure.title("Проверка создания пользователя с теми же данными")
    def test_create_user_with_same_creds(self, user_payload, delete_user):
        with allure.step("Создание пользователя"):
            status_code, response_body, token = CreateUser.post_create_user(payload=user_payload)
            delete_user.append(token)
        with allure.step("Регистрация пользователя с использованными данными"):
            status_code, response_body, token = CreateUser.post_create_user(payload=user_payload)
        with allure.step("Проверка, что статус код: 403"):
            assert status_code == 403
        with allure.step("Проверка, что параметр 'success': False"):
            assert response_body["success"] is False
        with allure.step("Проверка корректности сообщения"):
            assert response_body["message"] == IS_ALREADY_EXIST_MESSAGE

    @allure.title("Проверка обязательности полей")
    @pytest.mark.parametrize("email, password, name", [
        ("", create_fake_password(), create_fake_name()),
        (create_fake_email(), "", create_fake_name()),
        (create_fake_email(), create_fake_password(), "")
    ])
    def test_create_user_without_required_parameter(self, email, password, name):
        with allure.step(f"Формирование payload: email='{email}', password='{password}', name='{name}'"):
            payload = {
                "email": email,
                "password": password,
                "name": name
            }
        with allure.step(f"Регистрация пользователя с email='{email}', password='{password}', name='{name}'"):
            status_code, response_body, token = CreateUser.post_create_user(payload=payload)
        with allure.step("Проверка, что статус код: 403"):
            assert status_code == 403
        with allure.step("Проверка корректности сообщения"):
            assert response_body["message"] == REQUIRED_FIELDS_MESSAGE
