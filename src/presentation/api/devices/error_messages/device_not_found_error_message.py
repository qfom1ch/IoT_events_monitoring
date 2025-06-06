from pydantic import BaseModel, Field

from src.domain.devices.exceptions.device_not_found_error import DeviceNotFoundError


class ErrorMessageDeviceNotFound(BaseModel):
    detail: str = Field(examples=[DeviceNotFoundError.message])
