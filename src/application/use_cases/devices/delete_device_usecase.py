from abc import ABC, abstractmethod

from src.domain.devices.exceptions.device_not_found_error import DeviceNotFoundError
from src.domain.devices.interfaces.device_repo import DeviceRepository
from src.domain.devices.value_objects.device_id import DeviceId


class DeleteDeviceUseCase(ABC):
    @abstractmethod
    async def execute(self, device_id: DeviceId) -> None: ...


class DeleteDeviceUseCaseImpl(DeleteDeviceUseCase):
    def __init__(self, repository: DeviceRepository) -> None:
        self.repository = repository

    async def execute(self, device_id: DeviceId) -> None:
        device = await self.repository.find_by_id(device_id)

        if device is None:
            raise DeviceNotFoundError

        await self.repository.delete(device_id)


def new_delete_device_usecase(device_repository: DeviceRepository) -> DeleteDeviceUseCase:
    return DeleteDeviceUseCaseImpl(device_repository)
