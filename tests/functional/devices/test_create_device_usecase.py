import pytest

from src.domain.enums import SensorType


@pytest.mark.asyncio
async def test_create_device(async_client) -> None:
    # Arrange
    payload = {
        'name': 'Functional Test Device',
        'location': 'Functional Test Location',
        'sensor_type': SensorType.TEMPERATURE.value,
    }

    # Act
    response = await async_client.post('/devices', json=payload)

    # Assert
    assert response.status_code == 201
    data = response.json()
    assert data['name'] == 'Functional Test Device'
    assert data['location'] == 'Functional Test Location'
    assert data['sensor_type'] == SensorType.TEMPERATURE.value

    device_id = data['id']
    get_response = await async_client.get(f'/devices/{device_id}')
    assert get_response.status_code == 200
    assert get_response.json()['name'] == 'Functional Test Device'


@pytest.mark.asyncio
async def test_create_device_invalid_data(async_client) -> None:
    # Arrange
    invalid_payload = {'name': '', 'location': 'Test Location', 'sensor_type': 'INVALID_TYPE'}

    # Act
    response = await async_client.post('/devices', json=invalid_payload)

    # Assert
    assert response.status_code == 422
