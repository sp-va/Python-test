import pytest

from tests.conftest import client

@pytest.mark.run(order=6)
def test_registration_add():
    response = client.post(
        '/registration/add/',
        json={
            'user_id': 1,
            'picnic_id': 1
        }
    )

    assert response.status_code == 200

    data = response.json()
    assert data['user_id'] == 1
    assert data['picnic_id'] == 1

    