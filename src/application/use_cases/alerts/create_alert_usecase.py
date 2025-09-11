from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.alerts.entities.alert import Alert, AlertSeverity
from src.domain.alerts.interfaces.alert_repo import AlertRepository
from src.domain.alerts.interfaces.alert_search_repo import AlertSearchRepo


class CreateAlertUseCase(ABC):
    @abstractmethod
    async def execute(
        self, event_id: UUID, device_id: UUID, message: str, severity: AlertSeverity
    ) -> Alert: ...


class CreateAlertUseCaseImpl(CreateAlertUseCase):
    def __init__(self, repository: AlertRepository, search_repository: AlertSearchRepo) -> None:
        self.repository = repository
        self.search_repository = search_repository

    async def execute(
        self, event_id: UUID, device_id: UUID, message: str, severity: AlertSeverity
    ) -> Alert:
        alert = Alert.create(
            event_id=event_id, device_id=device_id, message=message, severity=severity
        )
        await self.repository.save(alert)
        await self.search_repository.bulk_add([alert])
        return alert
