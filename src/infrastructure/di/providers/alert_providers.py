from dishka import Provider, Scope, provide

from src.application.use_cases.alerts.create_alert_usecase import (
    CreateAlertUseCase,
    CreateAlertUseCaseImpl,
)
from src.application.use_cases.alerts.find_alert_by_id_usecase import (
    FindAlertByIdUseCase,
    FindAlertByIdUseCaseImpl,
)
from src.domain.alerts.interfaces.alert_repo import AlertRepository
from src.infrastructure.mongodb.alerts.alert_repo import MongoAlertRepository


class AlertProvider(Provider):
    scope = Scope.REQUEST

    alert_repo = provide(MongoAlertRepository, provides=AlertRepository)
    create_alert_usecase = provide(CreateAlertUseCaseImpl, provides=CreateAlertUseCase)
    find_alert_by_id_usecase = provide(FindAlertByIdUseCaseImpl, provides=FindAlertByIdUseCase)
