from datetime import datetime
from typing import Any

from pydantic import UUID4, BaseModel, Field

from src.domain.enums import SensorType


class SensorEventCreateSchema(BaseModel):
    device_id: UUID4
    sensor_type: SensorType
    value: float
    timestamp: datetime
    metadata: dict[str, Any] = Field(default_factory=dict)
