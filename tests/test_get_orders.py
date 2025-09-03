# tests/test_get_orders.py
import requests
import allure

BASE = "https://stellarburgers.nomoreparties.site/api"


@allure.epic("Stellar Burgers")
@allure.feature("Получение заказов")
class TestGetOrders:
    @allure.story("Авторизованный пользователь")
    @allure.title("Получение заказов авторизованного пользователя")
    def test_get_user_orders_authorized(self, new_user, ingredients_list):
        headers = {"Authorization": new_user["access"]}
        # создаём заказ, чтобы гарантировать запись
        requests.post(f"{BASE}/orders", headers=headers, json={"ingredients": ingredients_list[:2]})
        with allure.step("Отправляем GET-запрос /orders с авторизацией"):
            r = requests.get(f"{BASE}/orders", headers=headers)
            allure.attach(r.text, "Ответ сервера", allure.attachment_type.JSON)
        with allure.step("Проверяем успешное получение заказов"):
            assert r.status_code == 200
            js = r.json()
            assert js.get("success") is True
            assert isinstance(js.get("orders"), list)

    @allure.story("Неавторизованный пользователь")
    @allure.title("Получение заказов без авторизации → 401")
    def test_get_user_orders_unauthorized(self):
        with allure.step("Отправляем GET-запрос /orders без авторизации"):
            r = requests.get(f"{BASE}/orders")
            allure.attach(r.text, "Ответ сервера", allure.attachment_type.JSON)
        with allure.step("Проверяем, что сервер вернул ошибку 401"):
            assert r.status_code == 401
            js = r.json()
            assert js.get("success") is False
