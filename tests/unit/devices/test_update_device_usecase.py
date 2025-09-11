import pytest

from src.domain.devices.value_objects.device_id import DeviceId
from src.domain.enums import SensorType


@pytest.mark.asyncio
async def test_update_device_name_only(update_device_usecase, device_repository_mock, device) -> None:
    # Arrange
    device_repository_mock.find_by_id.return_value = device
    name = 'ChangedName'

    # Act
    result = await update_device_usecase.execute(device.id, name=name)

    # Assert
    assert result.name == name
    assert result.sensor_type == device.sensor_type
    assert result.location == device.location
    device_repository_mock.find_by_id.assert_called_once_with(device.id)
    device_repository_mock.update.assert_called_once_with(result)


@pytest.mark.asyncio
async def test_update_device_sensor_type_only(
    update_device_usecase, device_repository_mock, device
) -> None:
    # Arrange
    device_repository_mock.find_by_id.return_value = device

    # Act
    result = await update_device_usecase.execute(device.id, sensor_type=SensorType.HUMIDITY)

    # Assert
    assert result.sensor_type == SensorType.HUMIDITY
    assert result.name == device.name
    assert result.location == device.location
    device_repository_mock.find_by_id.assert_called_once_with(device.id)
    device_repository_mock.update.assert_called_once_with(result)


@pytest.mark.asyncio
async def test_update_device_all_fields(update_device_usecase, device_repository_mock, device) -> None:
    # Arrange
    device_repository_mock.find_by_id.return_value = device
    new_name = 'ChangedName'
    new_location = ('ChangedLocation',)

    # Act
    result = await update_device_usecase.execute(
        device.id, name=new_name, location=new_location, sensor_type=SensorType.HUMIDITY
    )

    # Assert
    assert result.name == new_name
    assert result.location == new_location
    assert result.sensor_type == SensorType.HUMIDITY
    device_repository_mock.find_by_id.assert_called_once_with(device.id)
    device_repository_mock.update.assert_called_once_with(result)


@pytest.mark.asyncio
async def test_update_device_not_found(update_device_usecase, device_repository_mock) -> None:
    # Arrange
    device_id = DeviceId.generate()
    device_repository_mock.find_by_id.return_value = None
    new_name = 'ChangedName'

    # Act & Assert
    with pytest.raises(Exception) as exc_info:
        await update_device_usecase.execute(device_id, name=new_name)
    assert 'Device not found' in str(exc_info.value)
