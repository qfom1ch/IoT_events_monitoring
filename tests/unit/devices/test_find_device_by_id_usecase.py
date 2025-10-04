import pytest

from src.domain.devices.value_objects.device_id import DeviceId


@pytest.mark.asyncio
async def test_find_device_by_id_success(
    find_device_by_id_usecase, device_repository_mock, device
) -> None:
    # Arrange
    device_repository_mock.find_by_id.return_value = device

    # Act
    result = await find_device_by_id_usecase.execute(device.id)

    # Assert
    assert result == device
    device_repository_mock.find_by_id.assert_called_once_with(device.id)


@pytest.mark.asyncio
async def test_find_device_by_id_not_found(
    find_device_by_id_usecase, device_repository_mock
) -> None:
    # Arrange
    device_id = DeviceId.generate()
    device_repository_mock.find_by_id.return_value = None

    # Act & Assert
    with pytest.raises(Exception) as exc_info:
        await find_device_by_id_usecase.execute(device_id)
    assert 'Device not found' in str(exc_info.value)
