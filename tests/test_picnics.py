import datetime as dt
import pytest

from tests.conftest import client

picnic_time = None

@pytest.mark.run(order=3)
def test_picnics_add():
    current_datetime = dt.datetime.now() + dt.timedelta(days=1)
    current_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    response = client.post(
        '/picnics/add/',
        json={
            "city_id": 1,
            'time': current_datetime
        }
    )
    assert response.status_code == 200

    data = response.json()
    global picnic_time
    picnic_time = data['time']
    assert data['id'] == 1
    assert data['city'] == 'Tyumen'

@pytest.mark.run(order=4)
def test_picnics_get():
    response = client.get(
        '/picnics/get/',
        params={'past': False, 'picnic_datetime': picnic_time}
    )

    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert data[0]['time'] == picnic_time
    assert data[0]['id'] == 1
    
