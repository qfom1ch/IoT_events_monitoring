from src.core.exceptions import AppException


class AlertNotFoundError(AppException):
    message = 'Alert not found'

    def __str__(self) -> str:
        return self.message
