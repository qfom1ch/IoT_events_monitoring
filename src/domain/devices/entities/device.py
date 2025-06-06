from dataclasses import dataclass

from src.domain.devices.value_objects.device_id import DeviceId
from src.domain.enums import SensorType


@dataclass(eq=False)
class Device:
    id: DeviceId
    name: str
    sensor_type: SensorType
    location: str
    is_active: bool = False

    def activate(self) -> None:
        self.is_active = True

    def deactivate(self) -> None:
        self.is_active = False

    def __str__(self) -> str:
        return f'Device(name: {self.name}, sensor_type: {self.sensor_type})'

    def __eq__(self, obj: object) -> bool:
        if isinstance(obj, Device):
            return self.id == obj.id

        return False

    @staticmethod
    def create(name: str, location: str, sensor_type: SensorType) -> 'Device':
        return Device(DeviceId.generate(), name, sensor_type, location, False)
