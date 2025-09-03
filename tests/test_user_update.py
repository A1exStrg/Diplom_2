# tests/test_user_update.py
import uuid
import requests
import allure

BASE = "https://stellarburgers.nomoreparties.site/api"


@allure.epic("Stellar Burgers")
@allure.feature("Обновление данных пользователя")
class TestUserUpdate:
    @allure.story("С авторизацией")
    @allure.title("Обновление данных с авторизацией")
    def test_update_user_authorized(self, new_user):
        # достаём accessToken из фикстуры нового пользователя
        access = new_user["access"]
        headers = {"Authorization": access}
        new_name = "Name_" + uuid.uuid4().hex[:6]

        with allure.step("Отправляем PATCH-запрос /auth/user с токеном и новым именем"):
            r = requests.patch(f"{BASE}/auth/user", headers=headers, json={"name": new_name})
            allure.attach(r.text, "Ответ сервера", allure.attachment_type.JSON)

        with allure.step("Проверяем успешный статус и обновление имени"):
            assert r.status_code == 200
            js = r.json()
            assert js.get("success") is True
            assert js.get("user", {}).get("name") == new_name

    @allure.story("Без авторизации")
    @allure.title("Обновление данных без авторизации → 401")
    def test_update_user_unauthorized(self):
        with allure.step("Отправляем PATCH-запрос /auth/user без токена"):
            r = requests.patch(f"{BASE}/auth/user", json={"name": "NoAuth"})
            allure.attach(r.text, "Ответ сервера", allure.attachment_type.JSON)

        with allure.step("Проверяем код 401 и сообщение об ошибке"):
            assert r.status_code == 401
            js = r.json()
            assert js.get("success") is False
            assert js.get("message") == "You should be authorised"
