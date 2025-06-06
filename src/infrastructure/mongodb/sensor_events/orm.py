from datetime import datetime
from typing import Any
from uuid import UUID

from beanie import Document
from pydantic import Field

from src.domain.devices.value_objects.device_id import DeviceId
from src.domain.enums import SensorType
from src.domain.sensor_events.entities.sensor_event import SensorEvent
from src.domain.sensor_events.value_objects.sensor_event_id import SensorEventId


class SensorEventDB(Document):
    id: UUID
    device_id: UUID
    sensor_type: str
    value: float
    timestamp: datetime
    metadata: dict[str, Any] = Field(default_factory=dict)

    class Settings:
        name = 'sensor_events'
        use_state_management = True

    def to_domain(self) -> SensorEvent:
        return SensorEvent(
            id=SensorEventId(self.id),
            device_id=DeviceId(self.device_id),
            sensor_type=SensorType(self.sensor_type),
            value=self.value,
            timestamp=self.timestamp,
            metadata=self.metadata or {},
        )

    @classmethod
    def from_domain(cls, sensor_event: SensorEvent) -> 'SensorEventDB':
        return cls(
            id=sensor_event.id.value,
            device_id=sensor_event.device_id.value,
            sensor_type=sensor_event.sensor_type.value,
            value=sensor_event.value,
            timestamp=sensor_event.timestamp,
            metadata=sensor_event.metadata,
        )
