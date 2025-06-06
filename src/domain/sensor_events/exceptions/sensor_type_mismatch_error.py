from src.core.exceptions import AppException


class SensorTypeMismatchError(AppException):
    message = 'Event sensor type does not match device sensor type'

    def __str__(self) -> str:
        return self.message
