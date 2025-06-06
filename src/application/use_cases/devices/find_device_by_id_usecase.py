from abc import ABC, abstractmethod

from src.domain.devices.entities.device import Device
from src.domain.devices.exceptions.device_not_found_error import DeviceNotFoundError
from src.domain.devices.interfaces.device_repo import DeviceRepository
from src.domain.devices.value_objects.device_id import DeviceId


class FindDeviceByIdUseCase(ABC):
    @abstractmethod
    async def execute(self, device_id: DeviceId) -> Device: ...


class FindDeviceByIdUseCaseImpl(FindDeviceByIdUseCase):
    def __init__(self, repository: DeviceRepository) -> None:
        self.repository = repository

    async def execute(self, device_id: DeviceId) -> Device:
        device: Device = await self.repository.find_by_id(device_id)
        if not device:
            raise DeviceNotFoundError
        return device


def new_find_device_by_id_usecase(device_repository: DeviceRepository) -> FindDeviceByIdUseCase:
    return FindDeviceByIdUseCaseImpl(device_repository)
