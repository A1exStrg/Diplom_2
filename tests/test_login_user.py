import requests
import allure
from url.url import BASE

@allure.epic("Stellar Burgers")
@allure.feature("Авторизация")
class TestAuth:
    @allure.story("Успешный вход")
    @allure.title("Логин под существующим пользователем")
    def test_login_existing_user(self, new_user):
        payload = {"email": new_user["email"], "password": new_user["password"]}
        with allure.step("Отправляем POST-запрос /auth/login с корректными данными"):
            r = requests.post(f"{BASE}/auth/login", json=payload)
            allure.attach(r.text, "Ответ сервера", allure.attachment_type.JSON)

        with allure.step("Проверяем успешный статус и наличие токена"):
            assert r.status_code == 200
            js = r.json()
            assert js.get("success") is True
            assert "accessToken" in js or "access" in js

    @allure.story("Ошибка входа")
    @allure.title("Логин с неверными данными → 401")
    def test_login_wrong_credentials(self):
        payload = {"email": "no_user@example.com", "password": "wrong"}
        with allure.step("Отправляем POST-запрос /auth/login с неверными данными"):
            r = requests.post(f"{BASE}/auth/login", json=payload)
            allure.attach(r.text, "Ответ сервера", allure.attachment_type.JSON)

        with allure.step("Проверяем код 401 и сообщение об ошибке"):
            assert r.status_code == 401
            js = r.json()
            assert js.get("success") is False
            assert js.get("message") == "email or password are incorrect"