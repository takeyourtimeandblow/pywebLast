import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_get_all_jobs(client):
    """Корректное получение всех работ"""
    response = client.get('/api/jobs')
    assert response.status_code == 200
    assert 'jobs' in response.json


def test_get_one_job_correct(client):
    """Корректное получение одной работы"""
    response = client.get('/api/jobs/1')
    assert response.status_code == 200
    assert 'job' in response.json


def test_get_one_job_wrong_id(client):
    """Ошибка: работа с таким id не существует"""
    response = client.get('/api/jobs/9999')
    assert response.status_code == 404
    assert response.json['error'] == 'Not found'


def test_get_one_job_string_id(client):
    """Ошибка: id передан строкой"""
    response = client.get('/api/jobs/abc')
    assert response.status_code == 404
