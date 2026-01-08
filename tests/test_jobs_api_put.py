import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_edit_job_correct(client):
    """Корректное редактирование работы"""
    response = client.put('/api/jobs/1', json={
        "work_size": 25,
        "is_finished": True
    })
    assert response.status_code == 200

    # Проверяем, что данные изменились
    response = client.get('/api/jobs/1')
    assert response.json['job']['work_size'] == 25
    assert response.json['job']['is_finished'] is True


def test_edit_job_wrong_id(client):
    """Некорректно: редактирование несуществующей работы"""
    response = client.put('/api/jobs/9999', json={
        "work_size": 10
    })
    assert response.status_code == 404


def test_edit_job_empty_request(client):
    """Некорректно: пустой запрос"""
    response = client.put('/api/jobs/1')
    assert response.status_code == 400
