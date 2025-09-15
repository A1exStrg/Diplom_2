import requests
import pytest
from url.url import BASE
from helpers import _rand

@pytest.fixture
def ingredients_list():
    r = requests.get(f"{BASE}/ingredients")
    body = r.json()
    items = body.get("data") or body.get("ingredients") or []
    ids = [it["_id"] for it in items]
    return ids

@pytest.fixture
def new_user():
    """
    Создаёт уникального пользователя и возвращает его данные и токены.
    В teardown удаляет пользователя, если вернулся access token.
    """
    email = f"stu_{_rand()}@example.com"
    password = f"Pass{_rand()}!"
    name = f"Student_{_rand()}"

    payload = {"email": email, "password": password, "name": name}

    r = requests.post(f"{BASE}/auth/register", json=payload)
    js = r.json()

    # accessToken в ответе приходит как "Bearer <token>"
    access = js.get("accessToken") or js.get("access")
    refresh = js.get("refreshToken") or js.get("refresh")
    yield {"email": email, "password": password, "name": name, "access": access, "refresh": refresh}

    # teardown: удалить пользователя, если есть access
    try:
        if access:
            requests.delete(f"{BASE}/auth/user", headers={"Authorization": access})
    except Exception:
        pass
