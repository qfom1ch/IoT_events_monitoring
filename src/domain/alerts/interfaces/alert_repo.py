from abc import ABC, abstractmethod

from src.domain.alerts.entities.alert import Alert
from src.domain.alerts.value_objects.alert_id import AlertId


class AlertRepository(ABC):
    @abstractmethod
    async def save(self, alert: Alert) -> None: ...

    @abstractmethod
    async def find_by_id(self, alert_id: AlertId) -> Alert | None: ...
