from abc import ABC, abstractmethod

from src.domain.alerts.entities.alert import Alert
from src.domain.alerts.exceptions.alert_not_found_error import AlertNotFoundError
from src.domain.alerts.interfaces.alert_repo import AlertRepository
from src.domain.alerts.value_objects.alert_id import AlertId


class FindAlertByIdUseCase(ABC):
    @abstractmethod
    async def execute(self, alert_id: AlertId) -> Alert: ...


class FindAlertByIdUseCaseImpl(FindAlertByIdUseCase):
    def __init__(self, repository: AlertRepository) -> None:
        self.repository = repository

    async def execute(self, alert_id: AlertId) -> Alert:
        alert: Alert = await self.repository.find_by_id(alert_id)
        if not alert:
            raise AlertNotFoundError
        return alert


def new_find_alert_by_id_usecase(alert_repository: AlertRepository) -> FindAlertByIdUseCase:
    return FindAlertByIdUseCaseImpl(alert_repository)
