from src.core.exceptions import AppException


class DeviceNotFoundError(AppException):
    message = 'Device not found'

    def __str__(self) -> str:
        return self.message
