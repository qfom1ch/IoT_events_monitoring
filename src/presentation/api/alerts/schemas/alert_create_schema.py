from pydantic import UUID4, BaseModel, Field

from src.domain.alerts.entities.alert import AlertSeverity


class AlertCreateSchema(BaseModel):
    event_id: UUID4
    device_id: UUID4
    message: str = Field(min_length=1, max_length=528)
    severity: AlertSeverity
