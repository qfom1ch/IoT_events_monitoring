from unittest.mock import Mock

import pytest

from src.application.use_cases.devices.create_device_usecase import CreateDeviceUseCaseImpl
from src.application.use_cases.devices.delete_device_usecase import DeleteDeviceUseCaseImpl
from src.application.use_cases.devices.find_device_by_id_usecase import (
    FindDeviceByIdUseCaseImpl,
)
from src.application.use_cases.devices.update_device_usecase import UpdateDeviceUseCaseImpl
from src.domain.devices.entities.device import Device
from src.domain.devices.interfaces.device_repo import DeviceRepository
from src.domain.devices.value_objects.device_id import DeviceId
from src.domain.enums import SensorType


@pytest.fixture
def device_repository_mock():
    return Mock(spec=DeviceRepository)


@pytest.fixture
def device():
    return Device(
        id=DeviceId.generate(),
        name='SomeName',
        location='some location',
        sensor_type=SensorType.TEMPERATURE,
    )


@pytest.fixture
def create_device_usecase(device_repository_mock):
    return CreateDeviceUseCaseImpl(device_repository_mock)


@pytest.fixture
def delete_device_usecase(device_repository_mock):
    return DeleteDeviceUseCaseImpl(device_repository_mock)


@pytest.fixture
def find_device_by_id_usecase(device_repository_mock):
    return FindDeviceByIdUseCaseImpl(device_repository_mock)


@pytest.fixture
def update_device_usecase(device_repository_mock):
    return UpdateDeviceUseCaseImpl(device_repository_mock)
