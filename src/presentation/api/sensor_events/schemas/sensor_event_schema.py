from datetime import datetime
from typing import Any

from pydantic import UUID4, BaseModel

from src.domain.enums import SensorType
from src.domain.sensor_events.entities.sensor_event import SensorEvent


class SensorEventSchema(BaseModel):
    id: UUID4
    device_id: UUID4
    sensor_type: SensorType
    value: float
    timestamp: datetime
    metadata: dict[str, Any]

    class Config:
        from_attributes = True

    @staticmethod
    def from_entity(sensor_event: SensorEvent) -> 'SensorEventSchema':
        return SensorEventSchema(
            id=sensor_event.id.value,
            device_id=sensor_event.device_id.value,
            sensor_type=sensor_event.sensor_type,
            value=sensor_event.value,
            timestamp=sensor_event.timestamp,
            metadata=sensor_event.metadata,
        )
