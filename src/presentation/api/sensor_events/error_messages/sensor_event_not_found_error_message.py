from pydantic import BaseModel, Field

from src.domain.sensor_events.exceptions.sensor_event_not_found_error import (
    SensorEventNotFoundError,
)


class ErrorMessageSensorEventNotFound(BaseModel):
    detail: str = Field(examples=[SensorEventNotFoundError.message])
