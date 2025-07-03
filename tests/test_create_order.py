import allure
from data.ingredients import INGREDIENTS, WRONG_INGREDIENTS
from data.messages import CREATE_ORDER_WITHOUT_INGREDIENTS_MESSAGE
from methods.create_order import CreateOrder
from methods.create_user import CreateUser
from methods.login_user import LoginUser


@allure.feature("Тесты на создание заказов")
class TestCreateOrder:

    @allure.title("Проверка создания заказа с токеном авторизации и ингредиентами")
    def test_create_order_with_token_and_ingredients(self, user_payload, delete_user):
        with allure.step("Создание пользователя"):
            status_code, response_body, token = CreateUser.post_create_user(payload=user_payload)
            delete_user.append(token)
        with allure.step("Авторизация пользователя"):
            _, _, token = LoginUser.post_login_user(payload=user_payload)
        with allure.step("Создание заказа авторизованным пользователем"):
            status_code, response_body = CreateOrder.post_create_order(ingredients=INGREDIENTS, token=token)
        with allure.step("Проверка, что статус код: 200"):
            assert status_code == 200
        with allure.step("Проверка, что параметр 'success': True"):
            assert response_body["success"] is True
        with allure.step("Проверка, что в ответе присутствует ID"):
            assert "number" in response_body["order"]

    @allure.title("Проверка создания заказа с токеном авторизации и без ингредиентов")
    def test_create_order_with_token_and_without_ingredients(self, user_payload, delete_user):
        with allure.step("Создание пользователя"):
            status_code, response_body, token = CreateUser.post_create_user(payload=user_payload)
            delete_user.append(token)
        with allure.step("Авторизация пользователя"):
            _, _, token = LoginUser.post_login_user(payload=user_payload)
        with allure.step("Создание заказа авторизованным пользователем"):
            status_code, response_body = CreateOrder.post_create_order(token=token)
        with allure.step("Проверка, что статус код: 400"):
            assert status_code == 400
        with allure.step("Проверка, что параметр 'success': False"):
            assert response_body["success"] is False
        with allure.step("Проверка корректности сообщения"):
            assert response_body["message"] == CREATE_ORDER_WITHOUT_INGREDIENTS_MESSAGE

    @allure.title("Проверка создания заказа без токена авторизации и с ингредиентами")
    def test_create_order_without_token_and_with_ingredients(self):
        with allure.step("Создание заказа без токена и с ингредиентами"):
            status_code, response_body = CreateOrder.post_create_order(ingredients=INGREDIENTS)
        with allure.step("Проверка, что статус код: 200"):
            assert status_code == 200
        with allure.step("Проверка, что параметр 'success': True"):
            assert response_body["success"] is True
        with allure.step("Проверка, что в ответе присутствует ID"):
            assert "number" in response_body["order"]

    @allure.title("Проверка создания заказа без токена авторизации и без ингредиентов")
    def test_create_order_without_token_and_without_ingredients(self):
        with allure.step("Создание заказа без токена и ингредиентов"):
            status_code, response_body = CreateOrder.post_create_order()
        with allure.step("Проверка, что статус код: 400"):
            assert status_code == 400
        with allure.step("Проверка, что параметр 'success': False"):
            assert response_body["success"] is False
        with allure.step("Проверка корректности сообщения"):
            assert response_body["message"] == CREATE_ORDER_WITHOUT_INGREDIENTS_MESSAGE

    @allure.title("Проверка создания заказа с токеном авторизации и неправильным хешем ингредиентов")
    def test_create_order_with_token_and_wrong_hash_ingredients(self, user_payload, delete_user):
        with allure.step("Создание пользователя"):
            status_code, response_body, token = CreateUser.post_create_user(payload=user_payload)
            delete_user.append(token)
        with allure.step("Авторизация пользователя"):
            _, _, token = LoginUser.post_login_user(payload=user_payload)
        with allure.step("Создание заказа авторизованным пользователем"):
            status_code, response_body = CreateOrder.post_create_order(ingredients=WRONG_INGREDIENTS, token=token)
        with allure.step("Проверка, что статус код: 200"):
            assert status_code == 500
