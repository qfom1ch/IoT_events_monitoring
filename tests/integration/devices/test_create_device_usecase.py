import pytest

from src.application.use_cases.devices.create_device_usecase import CreateDeviceUseCase
from src.domain.devices.entities.device import Device
from src.domain.devices.interfaces.device_repo import DeviceRepository
from src.domain.enums import SensorType


@pytest.mark.asyncio
async def test_create_device(container_test) -> None:
    usecase = await container_test.get(CreateDeviceUseCase)
    repository = await container_test.get(DeviceRepository)

    # Act
    result = await usecase.execute(
        name='Test Device', location='Test Location', sensor_type=SensorType.TEMPERATURE
    )

    # Assert
    assert isinstance(result, Device)
    assert result.name == 'Test Device'

    saved_device = await repository.find_by_id(result.id)
    assert saved_device is not None
    assert saved_device.name == 'Test Device'
