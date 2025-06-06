from datetime import datetime
from uuid import UUID

from beanie import Document

from src.domain.alerts.entities.alert import Alert, AlertSeverity
from src.domain.alerts.value_objects.alert_id import AlertId
from src.domain.devices.value_objects.device_id import DeviceId
from src.domain.sensor_events.value_objects.sensor_event_id import SensorEventId


class AlertDB(Document):
    id: UUID
    event_id: UUID
    device_id: UUID
    message: str
    severity: int
    created_at: datetime

    class Settings:
        name = 'alerts'
        use_state_management = True

    def to_domain(self) -> Alert:
        return Alert(
            id=AlertId(self.id),
            device_id=DeviceId(self.device_id),
            event_id=SensorEventId(self.event_id),
            message=self.message,
            severity=AlertSeverity(self.severity),
            created_at=self.created_at,
        )

    @classmethod
    def from_domain(cls, alert: Alert) -> 'AlertDB':
        return cls(
            id=alert.id.value,
            device_id=alert.device_id.value,
            event_id=alert.event_id.value,
            message=alert.message,
            severity=alert.severity.value,
            created_at=alert.created_at,
        )
