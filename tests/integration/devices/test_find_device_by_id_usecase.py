import pytest

from src.application.use_cases.devices.find_device_by_id_usecase import FindDeviceByIdUseCase
from src.domain.devices.entities.device import Device
from src.domain.devices.interfaces.device_repo import DeviceRepository
from src.domain.devices.value_objects.device_id import DeviceId
from src.domain.enums import SensorType


@pytest.mark.asyncio
async def test_find_device_by_id(container_test) -> None:
    # Arrange
    usecase = await container_test.get(FindDeviceByIdUseCase)
    repository = await container_test.get(DeviceRepository)

    device = Device(
        id=DeviceId.generate(),
        name='Test Device',
        location='Test Location',
        sensor_type=SensorType.TEMPERATURE,
    )
    await repository.save(device)

    # Act
    result = await usecase.execute(device.id)

    # Assert
    assert isinstance(result, Device)
    assert result.id == device.id
    assert result.name == device.name
    assert result.location == device.location
    assert result.sensor_type == device.sensor_type


@pytest.mark.asyncio
async def test_find_device_by_id_not_found(container_test) -> None:
    # Arrange
    usecase = await container_test.get(FindDeviceByIdUseCase)

    non_existent_id = DeviceId.generate()

    # Act & Assert
    with pytest.raises(Exception) as exc_info:
        await usecase.execute(non_existent_id)

    # Assert
    assert 'Device not found' in str(exc_info.value)
