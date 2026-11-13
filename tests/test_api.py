import sys
import os
# Добавляем корневую папку проекта в пути поиска Python
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import uuid
import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as test_client:
        yield test_client

# 1. Проверка доступности витрины каталога (веб-страница)
def test_web_catalog_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "Каталог электроники" in response.text

# 2. Проверка доступности Swagger UI
def test_swagger_docs_available(client):
    response = client.get("/docs")
    assert response.status_code == 200

# 3. Проверка получения списка товаров через REST API
def test_get_products_api(client):
    response = client.get("/product/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

# 4. Проверка фильтрации товаров по бренду
def test_filter_products_by_brand(client):
    response = client.get("/product/?brand=Apple")
    assert response.status_code == 200
    data = response.json()
    for product in data:
        assert product["brand"].lower() == "apple"

# 5. Сквозной тест: создание товара -> проверка -> удаление товара
def test_crud_product_lifecycle(client):
    unique_sku = f"TEST-{uuid.uuid4().hex[:6].upper()}"
    new_product = {
        "sku": unique_sku,
        "name": "Автотестовый смартфон",
        "brand": "Apple",
        "category": "Смартфоны",
        "price": 89990.0,
        "description": "Товар создан автоматически во время запуска pytest",
        "specifications": {
            "Экран": "6.1 дюйма",
            "Память": "128 ГБ"
        }
    }

    # 1. Создаем товар
    res_create = client.post("/product/new", json=new_product)
    assert res_create.status_code == 201
    product_id = res_create.json()["product_id"]

    # 2. Проверяем, что он появился по ID
    res_get = client.get(f"/product/{product_id}")
    assert res_get.status_code == 200
    assert res_get.json()["sku"] == unique_sku

    # 3. Удаляем за собой, чтобы не засорять базу
    res_delete = client.delete(f"/product/{product_id}")
    assert res_delete.status_code == 200

# 6. Проверка регистрации и авторизации пользователя
def test_user_signup_and_signin(client):
    unique_email = f"user_{uuid.uuid4().hex[:5]}@test.ru"
    user_payload = {
        "email": unique_email,
        "username": "Тестовый Пользователь",
        "role": "покупатель",
        "password": "testPassword123"
    }

    # Регистрация
    res_signup = client.post("/user/signup", json=user_payload)
    assert res_signup.status_code == 201

    # Вход в систему
    login_payload = {
        "email": unique_email,
        "password": "testPassword123"
    }
    res_signin = client.post("/user/signin", json=login_payload)
    assert res_signin.status_code == 200
