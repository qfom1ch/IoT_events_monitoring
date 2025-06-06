from pydantic import UUID4, BaseModel

from src.domain.devices.entities.device import Device
from src.domain.enums import SensorType


class DeviceSchema(BaseModel):
    id: UUID4
    name: str
    sensor_type: SensorType
    location: str
    is_active: bool

    class Config:
        from_attributes = True

    @staticmethod
    def from_entity(device: Device) -> 'DeviceSchema':
        return DeviceSchema(
            id=device.id.value,
            name=device.name,
            sensor_type=device.sensor_type,
            location=device.location,
            is_active=device.is_active,
        )
