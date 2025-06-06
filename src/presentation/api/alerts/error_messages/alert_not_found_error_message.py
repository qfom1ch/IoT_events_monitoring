from pydantic import BaseModel, Field

from src.domain.alerts.exceptions.alert_not_found_error import AlertNotFoundError


class ErrorMessageAlertNotFound(BaseModel):
    detail: str = Field(examples=[AlertNotFoundError.message])
