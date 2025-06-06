from abc import ABC, abstractmethod

from src.domain.devices.entities.device import Device
from src.domain.devices.exceptions.device_not_found_error import DeviceNotFoundError
from src.domain.devices.interfaces.device_repo import DeviceRepository
from src.domain.devices.value_objects.device_id import DeviceId
from src.domain.enums import SensorType


class UpdateDeviceUseCase(ABC):
    @abstractmethod
    async def execute(
        self,
        device_id: DeviceId,
        name: str | None = None,
        location: str | None = None,
        sensor_type: SensorType | None = None,
    ) -> Device: ...


class UpdateDeviceUseCaseImpl(UpdateDeviceUseCase):
    def __init__(self, repository: DeviceRepository) -> None:
        self.repository = repository

    async def execute(
        self,
        device_id: DeviceId,
        name: str | None = None,
        location: str | None = None,
        sensor_type: SensorType | None = None,
    ) -> Device:
        device: Device = await self.repository.find_by_id(device_id)
        if not device:
            raise DeviceNotFoundError

        if name:
            device.name = name

        if location:
            device.location = location

        if sensor_type:
            device.sensor_type = sensor_type

        await self.repository.update(device)

        return device


def new_update_device_usecase(device_repository: DeviceRepository) -> UpdateDeviceUseCase:
    return UpdateDeviceUseCaseImpl(device_repository)
