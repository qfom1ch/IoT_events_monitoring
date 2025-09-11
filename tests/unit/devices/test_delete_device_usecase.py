import pytest

from src.domain.devices.value_objects.device_id import DeviceId


@pytest.mark.asyncio
async def test_delete_device_success(delete_device_usecase, device_repository_mock, device) -> None:
    # Arrange
    device_repository_mock.find_by_id.return_value = device

    # Act
    await delete_device_usecase.execute(device.id)

    # Assert
    device_repository_mock.find_by_id.assert_called_once_with(device.id)
    device_repository_mock.delete.assert_called_once_with(device.id)


@pytest.mark.asyncio
async def test_delete_device_not_found(delete_device_usecase, device_repository_mock) -> None:
    # Arrange
    device_id = DeviceId.generate()
    device_repository_mock.find_by_id.return_value = None

    # Act & Assert
    with pytest.raises(Exception) as exc_info:
        await delete_device_usecase.execute(device_id)
    assert 'Device not found' in str(exc_info.value)
