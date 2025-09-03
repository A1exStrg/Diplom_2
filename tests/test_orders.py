import requests
import allure
import pytest

BASE = "https://stellarburgers.nomoreparties.site/api"


@allure.epic("Stellar Burgers")
@allure.feature("Создание заказа")
class TestOrders:

    @allure.story("Создание заказа с ингредиентами")
    @allure.title("Создание заказа с ингредиентами (без авторизации)")
    def test_create_order_with_ingredients(self, ingredients_list):
        payload = {"ingredients": ingredients_list[:2]}
        r = requests.post(f"{BASE}/orders", json=payload)
        assert r.status_code == 200
        js = r.json()
        assert js.get("success") is True

    @allure.story("Создание заказа авторизованным пользователем")
    @allure.title("Создание заказа с авторизацией")
    def test_create_order_with_auth(self, new_user, ingredients_list):
        headers = {"Authorization": new_user["access"]}
        payload = {"ingredients": ingredients_list[:2]}
        r = requests.post(f"{BASE}/orders", headers=headers, json=payload)
        assert r.status_code == 200
        js = r.json()
        assert js.get("success") is True

    @allure.story("Создание заказа без ингредиентов")
    @allure.title("Создание заказа без ингредиентов → 400")
    def test_create_order_without_ingredients(self, new_user):
        headers = {"Authorization": new_user["access"]}
        with allure.step("Отправляем POST-запрос /orders без списка ингредиентов"):
            r = requests.post(f"{BASE}/orders", headers=headers, json={})
            allure.attach(r.text, "Ответ сервера", allure.attachment_type.JSON)
        with allure.step("Проверяем, что вернулась ошибка 400"):
            assert r.status_code == 400
            js = r.json()
            assert js.get("success") is False
            assert js.get("message") == "Ingredient ids must be provided"

    @allure.story("Создание заказа с неверным ингредиентом")
    @allure.title("Создание заказа с неверным id ингредиента → 500")
    def test_create_order_with_invalid_ingredient(self, new_user):
        headers = {"Authorization": new_user["access"]}
        body = {"ingredients": ["12345abcdef"]}
        with allure.step("Отправляем POST-запрос /orders с несуществующим id ингредиента"):
            r = requests.post(f"{BASE}/orders", headers=headers, json=body)
            allure.attach(r.text, "Ответ сервера", allure.attachment_type.JSON)
        with allure.step("Проверяем, что сервер вернул 500"):
            assert r.status_code == 500
