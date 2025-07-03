import allure
from data.ingredients import INGREDIENTS, OTHER_INGREDIENTS
from data.messages import AUTHORIZATION_FALSE_MESSAGE
from methods.create_order import CreateOrder
from methods.create_user import CreateUser
from methods.get_orders import GetOrders
from methods.login_user import LoginUser


@allure.feature("Тесты на получение заказов конкретного пользователя")
class TestGetOrders:

    @allure.title("Проверка получения заказов пользователя с токеном авторизации")
    def test_get_user_orders_with_authorization(self, user_payload, delete_user):
        with allure.step("Создание пользователя"):
            status_code, response_body, token = CreateUser.post_create_user(payload=user_payload)
            delete_user.append(token)
        with allure.step("Авторизация пользователя"):
            _, _, token = LoginUser.post_login_user(payload=user_payload)
        with allure.step("Создание первого заказа авторизованным пользователем"):
            CreateOrder.post_create_order(ingredients=INGREDIENTS, token=token)
        with allure.step("Создание второго заказа авторизованным пользователем"):
            CreateOrder.post_create_order(ingredients=OTHER_INGREDIENTS, token=token)
        with allure.step("Получение информации о заказах пользователя"):
            status_code, response_body = GetOrders.get_user_orders(token=token)
        with allure.step("Проверка, что статус код: 200"):
            assert status_code == 200
        with allure.step("Проверка, что параметр 'success': True"):
            assert response_body["success"] is True
        with allure.step("Проверка, что вернулся непустой список orders"):
            orders = response_body.get("orders")
            assert isinstance(orders, list)
            assert len(orders) >= 2

    @allure.title("Проверка получения заказов пользователя без токена авторизации")
    def test_get_user_orders_without_authorization(self):
        with allure.step("Получение информации о заказах пользователя"):
            status_code, response_body = GetOrders.get_user_orders()
        with allure.step("Проверка, что статус код: 401"):
            assert status_code == 401
        with allure.step("Проверка, что параметр 'success': False"):
            assert response_body["success"] is False
        with allure.step("Проверка корректности сообщения"):
            assert response_body["message"] == AUTHORIZATION_FALSE_MESSAGE
