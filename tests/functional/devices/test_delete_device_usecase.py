import pytest

from src.domain.devices.value_objects.device_id import DeviceId
from src.domain.enums import SensorType


@pytest.mark.asyncio
async def test_delete_device(async_client) -> None:
    # Arrange
    create_payload = {
        'name': 'Device to Delete',
        'location': 'Some Location',
        'sensor_type': SensorType.HUMIDITY.value,
    }

    create_response = await async_client.post('/devices', json=create_payload)
    assert create_response.status_code == 201

    device_id = create_response.json()['id']

    # Act
    delete_response = await async_client.delete(f'/devices/{device_id}')

    # Assert
    assert delete_response.status_code == 204

    get_response = await async_client.get(f'/devices/{device_id}')
    assert get_response.status_code == 404


@pytest.mark.asyncio
async def test_delete_device_not_found(async_client) -> None:
    # Arrange
    non_existent_id = str(DeviceId.generate())

    # Act
    delete_response = await async_client.delete(f'/devices/{non_existent_id}')

    # Assert
    assert delete_response.status_code == 404

    error_data = delete_response.json()
    assert 'Device not found' in error_data['detail']
