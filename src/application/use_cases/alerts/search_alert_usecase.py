from abc import ABC, abstractmethod

from src.domain.alerts.entities.alert import Alert
from src.domain.alerts.interfaces.alert_search_repo import AlertSearchRepo
from src.infrastructure.elastic.alerts.schemas import AlertSearchQuery


class SearchAlertUseCase(ABC):
    @abstractmethod
    async def execute(self, query: AlertSearchQuery) -> list[Alert]: ...


class SearchAlertUseCaseImpl(SearchAlertUseCase):
    def __init__(self, repository: AlertSearchRepo) -> None:
        self.repository = repository

    async def execute(self, query: AlertSearchQuery) -> list[Alert]:
        return await self.repository.search(query)
