import pytest

from src.domain.devices.value_objects.device_id import DeviceId
from src.domain.enums import SensorType


@pytest.mark.asyncio
async def test_find_device_by_id(async_client) -> None:
    # Arrange
    create_payload = {
        'name': 'Test Device',
        'location': 'Test Location',
        'sensor_type': SensorType.TEMPERATURE.value,
    }

    create_response = await async_client.post('/devices', json=create_payload)
    assert create_response.status_code == 201
    created_device = create_response.json()
    device_id = created_device['id']

    # Act
    get_response = await async_client.get(f'/devices/{device_id}')

    # Assert
    assert get_response.status_code == 200
    retrieved_device = get_response.json()
    assert retrieved_device['id'] == device_id
    assert retrieved_device['name'] == 'Test Device'
    assert retrieved_device['location'] == 'Test Location'
    assert retrieved_device['sensor_type'] == SensorType.TEMPERATURE.value


@pytest.mark.asyncio
async def test_find_device_by_id_not_found(async_client) -> None:
    # Arrange
    non_existent_id = str(DeviceId.generate())

    # Act
    get_response = await async_client.get(f'/devices/{non_existent_id}')

    # Assert
    assert get_response.status_code == 404

    error_data = get_response.json()
    assert 'Device not found' in error_data['detail']
