import pytest

from src.domain.devices.value_objects.device_id import DeviceId
from src.domain.enums import SensorType


@pytest.mark.asyncio
async def test_update_device_name_only(async_client) -> None:
    # Arrange
    create_payload = {
        'name': 'Original Name',
        'location': 'Original Location',
        'sensor_type': SensorType.TEMPERATURE.value,
    }

    create_response = await async_client.post('/devices', json=create_payload)
    assert create_response.status_code == 201
    original_device = create_response.json()
    device_id = original_device['id']

    # Act
    update_payload = {'name': 'Changed Name'}

    update_response = await async_client.put(f'/devices/{device_id}', json=update_payload)

    # Assert
    assert update_response.status_code == 200
    updated_device = update_response.json()
    assert updated_device['name'] == 'Changed Name'
    assert updated_device['location'] == 'Original Location'
    assert updated_device['sensor_type'] == SensorType.TEMPERATURE.value

    get_response = await async_client.get(f'/devices/{device_id}')
    assert get_response.status_code == 200
    saved_device = get_response.json()
    assert saved_device['name'] == 'Changed Name'
    assert saved_device['location'] == 'Original Location'
    assert saved_device['sensor_type'] == SensorType.TEMPERATURE.value


@pytest.mark.asyncio
async def test_update_device_sensor_type_only(async_client) -> None:
    # Arrange
    create_payload = {
        'name': 'Original Name',
        'location': 'Original Location',
        'sensor_type': SensorType.TEMPERATURE.value,
    }

    create_response = await async_client.post('/devices', json=create_payload)
    assert create_response.status_code == 201
    original_device = create_response.json()
    device_id = original_device['id']

    # Act
    update_payload = {'sensor_type': SensorType.HUMIDITY.value}

    update_response = await async_client.put(f'/devices/{device_id}', json=update_payload)

    # Assert
    assert update_response.status_code == 200
    updated_device = update_response.json()
    assert updated_device['sensor_type'] == SensorType.HUMIDITY.value
    assert updated_device['name'] == 'Original Name'
    assert updated_device['location'] == 'Original Location'

    get_response = await async_client.get(f'/devices/{device_id}')
    assert get_response.status_code == 200
    saved_device = get_response.json()
    assert saved_device['sensor_type'] == SensorType.HUMIDITY.value
    assert saved_device['name'] == 'Original Name'
    assert saved_device['location'] == 'Original Location'


@pytest.mark.asyncio
async def test_update_device_all_fields(async_client) -> None:
    # Arrange
    create_payload = {
        'name': 'Original Name',
        'location': 'Original Location',
        'sensor_type': SensorType.TEMPERATURE.value,
    }

    create_response = await async_client.post('/devices', json=create_payload)
    assert create_response.status_code == 201
    original_device = create_response.json()
    device_id = original_device['id']

    # Act
    update_payload = {
        'name': 'Changed Name',
        'location': 'Changed Location',
        'sensor_type': SensorType.HUMIDITY.value,
    }

    update_response = await async_client.put(f'/devices/{device_id}', json=update_payload)

    # Assert
    assert update_response.status_code == 200
    updated_device = update_response.json()
    assert updated_device['name'] == 'Changed Name'
    assert updated_device['location'] == 'Changed Location'
    assert updated_device['sensor_type'] == SensorType.HUMIDITY.value

    get_response = await async_client.get(f'/devices/{device_id}')
    assert get_response.status_code == 200
    saved_device = get_response.json()
    assert saved_device['name'] == 'Changed Name'
    assert saved_device['location'] == 'Changed Location'
    assert saved_device['sensor_type'] == SensorType.HUMIDITY.value


@pytest.mark.asyncio
async def test_update_device_not_found(async_client) -> None:
    # Arrange
    non_existent_id = str(DeviceId.generate())
    update_payload = {'name': 'Changed Name'}

    # Act
    update_response = await async_client.put(f'/devices/{non_existent_id}', json=update_payload)

    # Assert
    assert update_response.status_code == 404

    error_data = update_response.json()
    assert 'detail' in error_data


@pytest.mark.asyncio
async def test_update_device_invalid_data(async_client) -> None:
    # Arrange
    create_payload = {
        'name': 'Original Name',
        'location': 'Original Location',
        'sensor_type': SensorType.TEMPERATURE.value,
    }

    create_response = await async_client.post('/devices', json=create_payload)
    assert create_response.status_code == 201
    device_id = create_response.json()['id']

    # Arrange
    invalid_payload = {'name': '', 'sensor_type': 'INVALID_TYPE'}

    # Act
    update_response = await async_client.put(f'/devices/{device_id}', json=invalid_payload)

    # Assert
    assert update_response.status_code == 422
