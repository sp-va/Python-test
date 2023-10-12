import pytest

from tests.conftest import client
@pytest.mark.run(order=1)
def test_cities_add(create_test_database):
    response = client.post(
        '/cities/add/',
        json={
            'name': 'Tyumen'
        }
    )
    
    assert response.status_code == 200
    
    data = response.json()
    assert data['id'] == 1
    assert data['name'] == 'Tyumen'
    assert isinstance(data['weather'], float)

@pytest.mark.run(order=2)
def test_cities_get():
    response = client.get('/cities/get/')
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1

    for obj in data:
        assert isinstance(obj['id'], int)
        assert isinstance(obj['name'], str)
        assert isinstance(obj['weather'], float)