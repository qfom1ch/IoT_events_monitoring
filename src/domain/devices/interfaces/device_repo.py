from abc import ABC, abstractmethod

from src.domain.devices.entities.device import Device
from src.domain.devices.value_objects.device_id import DeviceId


class DeviceRepository(ABC):
    @abstractmethod
    async def save(self, device: Device) -> None: ...

    @abstractmethod
    async def find_by_id(self, device_id: DeviceId) -> Device | None: ...

    @abstractmethod
    async def update(self, device: Device) -> None: ...

    @abstractmethod
    async def delete(self, device_id: DeviceId) -> None: ...
