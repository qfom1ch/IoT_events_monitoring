from pydantic import BaseModel, Field

from src.domain.enums import SensorType


class DeviceUpdateSchema(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    sensor_type: SensorType | None = None
    location: str = Field(default=None, min_length=1, max_length=100)
