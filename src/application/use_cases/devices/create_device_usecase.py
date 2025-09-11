from abc import ABC, abstractmethod

from src.domain.devices.entities.device import Device
from src.domain.devices.interfaces.device_repo import DeviceRepository
from src.domain.enums import SensorType


class CreateDeviceUseCase(ABC):
    @abstractmethod
    async def execute(self, name: str, location: str, sensor_type: SensorType) -> Device: ...


class CreateDeviceUseCaseImpl(CreateDeviceUseCase):
    def __init__(self, repository: DeviceRepository) -> None:
        self.repository = repository

    async def execute(self, name: str, location: str, sensor_type: SensorType) -> Device:
        device = Device.create(name=name, location=location, sensor_type=sensor_type)
        await self.repository.save(device)
        return device
