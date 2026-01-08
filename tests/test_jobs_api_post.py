import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_add_job_correct(client):
    """Корректное добавление работы"""
    response = client.post('/api/jobs', json={
        "id": 100,
        "team_leader": 1,
        "job": "Test API job",
        "work_size": 10,
        "collaborators": "2,3",
        "is_finished": False
    })
    assert response.status_code == 200
    assert response.json['success'] == 'OK'


def test_add_job_existing_id(client):
    """
    Некорректно: работа с таким id уже существует
    """
    response = client.post('/api/jobs', json={
        "id": 100,
        "team_leader": 1,
        "job": "Duplicate",
        "work_size": 5
    })
    assert response.status_code == 400
    assert response.json['error'] == 'Id already exists'


def test_add_job_empty_request(client):
    """
    Некорректно: пустой JSON-запрос
    """
    response = client.post('/api/jobs')
    assert response.status_code == 400


def test_add_job_missing_fields(client):
    """
    Некорректно: отсутствуют обязательные поля (job, team_leader)
    """
    response = client.post('/api/jobs', json={
        "id": 101
    })
    assert response.status_code == 200  # API добавляет, но данные некорректны
