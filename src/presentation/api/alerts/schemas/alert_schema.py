from datetime import datetime

from pydantic import UUID4, BaseModel

from src.domain.alerts.entities.alert import Alert, AlertSeverity


class AlertSchema(BaseModel):
    id: UUID4
    event_id: UUID4
    device_id: UUID4
    message: str
    severity: AlertSeverity
    created_at: datetime

    class Config:
        from_attributes = True

    @staticmethod
    def from_entity(alert: Alert) -> 'AlertSchema':
        return AlertSchema(
            id=alert.id.value,
            event_id=alert.event_id.value,
            device_id=alert.device_id.value,
            message=alert.message,
            severity=alert.severity,
            created_at=alert.created_at,
        )
