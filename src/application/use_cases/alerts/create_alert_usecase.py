from abc import abstractmethod
from uuid import UUID

from src.domain.alerts.entities.alert import Alert, AlertSeverity
from src.domain.alerts.interfaces.alert_repo import AlertRepository


class CreateAlertUseCase:
    @abstractmethod
    async def execute(
        self, event_id: UUID, device_id: UUID, message: str, severity: AlertSeverity
    ) -> Alert: ...


class CreateAlertUseCaseImpl(CreateAlertUseCase):
    def __init__(self, repository: AlertRepository) -> None:
        self.repository = repository

    async def execute(
        self, event_id: UUID, device_id: UUID, message: str, severity: AlertSeverity
    ) -> Alert:
        alert = Alert.create(
            event_id=event_id, device_id=device_id, message=message, severity=severity
        )
        await self.repository.save(alert)
        return alert
