import pytest

from src.domain.devices.entities.device import Device
from src.domain.enums import SensorType


@pytest.mark.asyncio
async def test_create_device(create_device_usecase, device_repository_mock) -> None:
    # Arrange
    result = await create_device_usecase.execute(
        name='SomeName', location='some location', sensor_type=SensorType.TEMPERATURE
    )

    # Assert
    assert isinstance(result, Device)
    assert result.name == 'SomeName'
    assert result.location == 'some location'
    assert result.sensor_type == SensorType.TEMPERATURE
    device_repository_mock.save.assert_called_once_with(result)


@pytest.mark.asyncio
async def test_create_repository_error(create_device_usecase, device_repository_mock) -> None:
    # Arrange
    device_repository_mock.save.side_effect = Exception('Database error')

    # Act & Assert
    with pytest.raises(Exception) as exc_info:
        await create_device_usecase.execute(
            name='SomeName', location='some location', sensor_type=SensorType.TEMPERATURE
        )
    assert str(exc_info.value) == 'Database error'
