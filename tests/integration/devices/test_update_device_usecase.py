import pytest

from src.application.use_cases.devices.update_device_usecase import UpdateDeviceUseCase
from src.domain.devices.entities.device import Device
from src.domain.devices.interfaces.device_repo import DeviceRepository
from src.domain.devices.value_objects.device_id import DeviceId
from src.domain.enums import SensorType


@pytest.mark.asyncio
async def test_update_device_name_only(container_test) -> None:
    # Arrange
    usecase = await container_test.get(UpdateDeviceUseCase)
    repository = await container_test.get(DeviceRepository)

    original_device = Device(
        id=DeviceId.generate(),
        name='Original Name',
        location='Original Location',
        sensor_type=SensorType.TEMPERATURE,
    )
    await repository.save(original_device)

    # Act
    updated_device = await usecase.execute(original_device.id, name='Changed Name')

    # Assert
    assert updated_device.name == 'Changed Name'
    assert updated_device.location == original_device.location
    assert updated_device.sensor_type == original_device.sensor_type

    saved_device = await repository.find_by_id(original_device.id)
    assert saved_device.name == 'Changed Name'
    assert saved_device.location == original_device.location
    assert saved_device.sensor_type == original_device.sensor_type


@pytest.mark.asyncio
async def test_update_device_sensor_type_only_integration(container_test) -> None:
    # Arrange
    usecase = await container_test.get(UpdateDeviceUseCase)
    repository = await container_test.get(DeviceRepository)

    # Создаем и сохраняем устройство
    original_device = Device(
        id=DeviceId.generate(),
        name='Original Name',
        location='Original Location',
        sensor_type=SensorType.TEMPERATURE,
    )
    await repository.save(original_device)

    # Act
    updated_device = await usecase.execute(original_device.id, sensor_type=SensorType.HUMIDITY)

    # Assert
    assert updated_device.sensor_type == SensorType.HUMIDITY
    assert updated_device.name == original_device.name
    assert updated_device.location == original_device.location

    saved_device = await repository.find_by_id(original_device.id)
    assert saved_device.sensor_type == SensorType.HUMIDITY
    assert saved_device.name == original_device.name
    assert saved_device.location == original_device.location


@pytest.mark.asyncio
async def test_update_device_all_fields_integration(container_test) -> None:
    # Arrange
    usecase = await container_test.get(UpdateDeviceUseCase)
    repository = await container_test.get(DeviceRepository)

    original_device = Device(
        id=DeviceId.generate(),
        name='Original Name',
        location='Original Location',
        sensor_type=SensorType.TEMPERATURE,
    )
    await repository.save(original_device)

    # Act
    updated_device = await usecase.execute(
        original_device.id,
        name='Changed Name',
        location='Changed Location',
        sensor_type=SensorType.HUMIDITY,
    )

    # Assert
    assert updated_device.name
