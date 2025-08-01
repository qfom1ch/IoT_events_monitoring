from abc import ABC, abstractmethod

from src.domain.alerts.entities.alert import Alert
from src.infrastructure.elastic.alerts.schemas import AlertSearchQuery


class AlertSearchRepo(ABC):
    @abstractmethod
    async def search(self, query: AlertSearchQuery) -> list[Alert]: ...

    @abstractmethod
    async def bulk_add(self, alerts: list[Alert]) -> None: ...

    @abstractmethod
    async def delete(self, alert_id: str) -> None: ...

    @abstractmethod
    async def update(self, alert: Alert) -> None: ...
