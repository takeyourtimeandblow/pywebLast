import pytest
from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


# ===============================
# 1. Получение пользователей
# ===============================

def test_get_all_users(client):
    response = client.get('/api/users')
    assert response.status_code == 200
    assert 'users' in response.json
    assert isinstance(response.json['users'], list)


def test_get_one_user_correct(client):
    response = client.get('/api/users/1')
    assert response.status_code == 200
    assert response.json['user']['id'] == 1


def test_get_one_user_wrong_id(client):
    response = client.get('/api/users/9999')
    assert response.status_code == 404


def test_get_one_user_string_id(client):
    response = client.get('/api/users/abc')
    assert response.status_code == 404


# ===============================
# 2. Добавление пользователя
# ===============================

def test_add_user_correct(client):
    response = client.post(
        '/api/users',
        json={
            "id": 100,
            "surname": "Test",
            "name": "User",
            "age": 30,
            "position": "tester",
            "speciality": "qa",
            "address": "module_test",
            "email": "test_user@mars.org",
            "password": "12345",
            "city_from": "TestCity"
        }
    )
    assert response.status_code == 200
    assert response.json['success'] is True


def test_add_user_without_email(client):
    # ❌ Некорректно: отсутствует обязательное поле email
    response = client.post(
        '/api/users',
        json={
            "id": 101,
            "surname": "NoEmail",
            "name": "User",
            "age": 25,
            "position": "tester",
            "speciality": "qa",
            "address": "module_test",
            "password": "12345"
        }
    )
    assert response.status_code == 400


def test_add_user_existing_id(client):
    # ❌ Некорректно: пользователь с таким id уже существует
    response = client.post(
        '/api/users',
        json={
            "id": 1,
            "surname": "Duplicate",
            "name": "User",
            "age": 30,
            "position": "tester",
            "speciality": "qa",
            "address": "module_test",
            "email": "duplicate@mars.org",
            "password": "12345"
        }
    )
    assert response.status_code == 400


def test_add_user_without_password(client):
    # ❌ Некорректно: отсутствует пароль
    response = client.post(
        '/api/users',
        json={
            "id": 102,
            "surname": "NoPassword",
            "name": "User",
            "age": 22,
            "position": "tester",
            "speciality": "qa",
            "address": "module_test",
            "email": "nopassword@mars.org"
        }
    )
    assert response.status_code == 400


# ===============================
# 3. Удаление пользователя
# ===============================

def test_delete_user_correct(client):
    response = client.delete('/api/users/100')
    assert response.status_code == 200

    # Проверяем, что пользователь удалён
    response = client.get('/api/users/100')
    assert response.status_code == 404


def test_delete_user_wrong_id(client):
    response = client.delete('/api/users/9999')
    assert response.status_code == 404


def test_delete_user_string_id(client):
    response = client.delete('/api/users/abc')
    assert response.status_code == 404


# ===============================
# 4. Редактирование пользователя
# ===============================

def test_edit_user_correct(client):
    response = client.put(
        '/api/users/2',
        json={
            "surname": "Lewis",
            "name": "Mark",
            "age": 35,
            "position": "chief engineer"
        }
    )
    assert response.status_code == 200

    # Проверяем, что данные изменились
    response = client.get('/api/users/2')
    assert response.json['user']['position'] == "chief engineer"


def test_edit_user_wrong_id(client):
    response = client.put(
        '/api/users/9999',
        json={"surname": "Ghost"}
    )
    assert response.status_code == 404


def test_edit_user_empty_request(client):
    # ❌ Некорректно: пустой запрос
    response = client.put('/api/users/2', json={})
    assert response.status_code == 400
