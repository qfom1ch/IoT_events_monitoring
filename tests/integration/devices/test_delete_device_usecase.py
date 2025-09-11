import pytest

from src.application.use_cases.devices.delete_device_usecase import DeleteDeviceUseCase
from src.domain.devices.entities.device import Device
from src.domain.devices.interfaces.device_repo import DeviceRepository
from src.domain.devices.value_objects.device_id import DeviceId
from src.domain.enums import SensorType


@pytest.mark.asyncio
async def test_delete_device(container_test) -> None:
    # Arrange
    usecase = await container_test.get(DeleteDeviceUseCase)
    repository = await container_test.get(DeviceRepository)

    device = Device(
        id=DeviceId.generate(),
        name='Device to Delete',
        location='Some Location',
        sensor_type=SensorType.HUMIDITY,
    )
    await repository.save(device)

    # Act
    await usecase.execute(device.id)

    # Assert
    deleted_device = await repository.find_by_id(device.id)
    assert deleted_device is None


@pytest.mark.asyncio
async def test_delete_device_not_found(container_test) -> None:
    # Arrange
    usecase = await container_test.get(DeleteDeviceUseCase)

    non_existent_id = DeviceId.generate()

    # Act & Assert
    with pytest.raises(Exception) as exc_info:
        await usecase.execute(non_existent_id)

    assert 'Device not found' in str(exc_info.value)
