import pytest

from tests.conftest import client

@pytest.mark.run(order=5)
def test_users_add():
    response = client.post(
        '/users/add/',
        json={
            'name': 'Name 1',
            'surname': 'Surname 1',
            'age': 20
        }
    )

    assert response.status_code == 200

    data = response.json()
    assert data['id'] == 1
    assert data['name'] == 'Name 1'
    assert data['surname'] == 'Surname 1'
    assert data['age'] == 20

@pytest.mark.run(order=7)
def test_users_get():
    response = client.get(
        '/users/get/',
        params={'min_age': 10, 'max_age': 50}
    )

    assert response.status_code == 200

    data = response.json()
    assert data[0]['id'] == 1
    assert data[0]['name'] == 'Name 1'
    assert data[0]['surname'] == 'Surname 1'
    assert data[0]['age'] == 20