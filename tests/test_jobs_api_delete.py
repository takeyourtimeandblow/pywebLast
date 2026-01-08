import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_delete_job_correct(client):
    """Корректное удаление работы"""
    response = client.delete('/api/jobs/100')
    assert response.status_code == 200
    assert response.json['success'] == 'OK'

    # Проверяем, что работа действительно удалена
    response = client.get('/api/jobs')
    ids = [job['id'] for job in response.json['jobs']]
    assert 100 not in ids


def test_delete_job_wrong_id(client):
    """Некорректно: попытка удалить несуществующую работу"""
    response = client.delete('/api/jobs/9999')
    assert response.status_code == 404
    assert response.json['error'] == 'Not found'
