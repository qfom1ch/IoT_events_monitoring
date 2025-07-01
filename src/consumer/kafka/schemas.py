from uuid import UUID

from pydantic import BaseModel, Field

from src.domain.enums import SensorType


class KafkaSensorEventMessage(BaseModel):
    device_id: UUID
    sensor_type: SensorType
    value: float
    metadata: dict = Field(default_factory=dict)
