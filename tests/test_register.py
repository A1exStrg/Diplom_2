# tests/test_register.py
import requests
import allure
import uuid
from faker import Faker

fake = Faker()
BASE_URL = "https://stellarburgers.nomoreparties.site/api"


@allure.epic("Stellar Burgers")
@allure.feature("Регистрация")
class TestUserRegistration:

    @allure.story("Регистрация нового пользователя")
    @allure.title("Создание уникального пользователя")
    def test_create_unique_user(self):
        unique_email = f"{uuid.uuid4().hex[:8]}_{fake.email()}"
        payload = {
            "email": unique_email,
            "password": "Password12345",
            "name": "TestUser"
        }
        with allure.step("Отправляем POST /auth/register с уникальными данными"):
            response = requests.post(f"{BASE_URL}/auth/register", json=payload)
            allure.attach(response.text, "response", allure.attachment_type.JSON)

        assert response.status_code == 200, f"Ошибка {response.status_code}: {response.text}"
        js = response.json()
        assert js.get("success") is True

    @allure.story("Регистрация существующего пользователя")
    @allure.title("Создание пользователя, который уже зарегистрирован → 403")
    def test_create_existing_user(self):
        email = f"{uuid.uuid4().hex[:8]}_{fake.email()}"
        payload = {"email": email, "password": "Password12345", "name": "DupUser"}

        # первый запрос создаёт пользователя
        requests.post(f"{BASE_URL}/auth/register", json=payload)

        # второй должен вернуть ошибку
        with allure.step("Отправляем POST /auth/register с теми же данными"):
            response = requests.post(f"{BASE_URL}/auth/register", json=payload)
            allure.attach(response.text, "response", allure.attachment_type.JSON)

        assert response.status_code == 403
        js = response.json()
        assert js.get("success") is False
        assert "already exists" in js.get("message", "")

    @allure.story("Регистрация с пустым полем")
    @allure.title("Создание пользователя без обязательного поля → 403")
    def test_create_user_without_required_field(self):
        payload = {
            # email специально не указываем
            "password": "Password12345",
            "name": "NoEmailUser"
        }
        with allure.step("Отправляем POST /auth/register без email"):
            response = requests.post(f"{BASE_URL}/auth/register", json=payload)
            allure.attach(response.text, "response", allure.attachment_type.JSON)

        assert response.status_code == 403
        js = response.json()
        assert js.get("success") is False
        assert "email" in js.get("message", "").lower()
