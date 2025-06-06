from pydantic import BaseModel, Field

from src.domain.enums import SensorType


class DeviceCreateSchema(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    sensor_type: SensorType
    location: str = Field(min_length=1, max_length=100)
