from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from uuid import UUID

from src.domain.devices.value_objects.device_id import DeviceId
from src.domain.enums import SensorType
from src.domain.sensor_events.value_objects.sensor_event_id import SensorEventId


@dataclass(eq=False)
class SensorEvent:
    id: SensorEventId
    device_id: DeviceId
    sensor_type: SensorType
    value: float
    timestamp: datetime
    metadata: dict[str, Any] = field(default_factory=dict)

    def __str__(self) -> str:
        return (
            f'SensorEvent(device_id={self.device_id},'
            f' sensor_type={self.sensor_type}, value={self.value})'
        )

    def __eq__(self, obj: object) -> bool:
        if isinstance(obj, SensorEvent):
            return self.id == obj.id

        return False

    @staticmethod
    def create(
        device_id: UUID,
        sensor_type: SensorType,
        value: float,
        metadata: dict[str, Any] | None = None,
    ) -> 'SensorEvent':
        return SensorEvent(
            SensorEventId.generate(),
            DeviceId(device_id),
            sensor_type,
            value,
            datetime.now(),
            metadata or {},
        )
