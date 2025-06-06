from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from uuid import UUID

from src.domain.alerts.value_objects.alert_id import AlertId
from src.domain.devices.value_objects.device_id import DeviceId
from src.domain.sensor_events.value_objects.sensor_event_id import SensorEventId


class AlertSeverity(int, Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


@dataclass(eq=False)
class Alert:
    id: AlertId
    event_id: SensorEventId
    device_id: DeviceId
    message: str
    severity: AlertSeverity
    created_at: datetime

    @property
    def severity_label(self) -> str:
        return self.severity.name

    @property
    def is_recent(self) -> bool:
        return datetime.now() - self.created_at < timedelta(hours=24)

    def __str__(self) -> str:
        return (
            f'Alert(severity={self.severity.name},'
            f' device={self.device_id}, message="{self.message}")'
        )

    def __eq__(self, obj: object) -> bool:
        if isinstance(obj, Alert):
            return self.id == obj.id

        return False

    @staticmethod
    def create(
        event_id: UUID, device_id: UUID, message: str, severity: AlertSeverity
    ) -> 'Alert':
        return Alert(
            AlertId.generate(),
            SensorEventId(event_id),
            DeviceId(device_id),
            message,
            severity,
            datetime.now(),
        )
