from uuid import UUID

from beanie import Document

from src.domain.devices.entities.device import Device
from src.domain.devices.value_objects.device_id import DeviceId
from src.domain.enums import SensorType


class DeviceDB(Document):
    id: UUID
    name: str
    sensor_type: str
    location: str
    is_active: bool = True

    class Settings:
        name = 'devices'
        use_state_management = True

    def to_domain(self) -> Device:
        return Device(
            id=DeviceId(self.id),
            name=self.name,
            sensor_type=SensorType(self.sensor_type),
            location=self.location,
            is_active=self.is_active,
        )

    @classmethod
    def from_domain(cls, device: Device) -> 'DeviceDB':
        return cls(
            id=device.id.value,
            name=device.name,
            sensor_type=device.sensor_type.value,
            location=device.location,
            is_active=device.is_active,
        )
