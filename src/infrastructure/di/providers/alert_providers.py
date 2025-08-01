from dishka import Provider, Scope, provide

from src.application.use_cases.alerts.create_alert_usecase import (
    CreateAlertUseCase,
    CreateAlertUseCaseImpl,
)
from src.application.use_cases.alerts.find_alert_by_id_usecase import (
    FindAlertByIdUseCase,
    FindAlertByIdUseCaseImpl,
)
from src.application.use_cases.alerts.search_alert_usecase import (
    SearchAlertUseCase,
    SearchAlertUseCaseImpl,
)
from src.domain.alerts.interfaces.alert_repo import AlertRepository
from src.domain.alerts.interfaces.alert_search_repo import AlertSearchRepo
from src.infrastructure.elastic.alerts.repo import ElasticAlertSearchRepo
from src.infrastructure.mongodb.alerts.alert_repo import MongoAlertRepository


class AlertProvider(Provider):
    scope = Scope.REQUEST

    alert_repo = provide(MongoAlertRepository, provides=AlertRepository)
    alert_search_repo = provide(ElasticAlertSearchRepo, provides=AlertSearchRepo)
    create_alert_usecase = provide(CreateAlertUseCaseImpl, provides=CreateAlertUseCase)
    find_alert_by_id_usecase = provide(FindAlertByIdUseCaseImpl, provides=FindAlertByIdUseCase)
    search_usecase = provide(SearchAlertUseCaseImpl, provides=SearchAlertUseCase)
