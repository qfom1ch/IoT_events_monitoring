from src.core.exceptions import AppException


class SensorEventNotFoundError(AppException):
    message = 'Sensor event not found'

    def __str__(self) -> str:
        return self.message
