from fastapi import Depends

from src.application.use_cases.alerts.create_alert_usecase import (
    CreateAlertUseCase,
    new_create_alert_usecase,
)
from src.application.use_cases.alerts.find_alert_by_id_usecase import (
    FindAlertByIdUseCase,
    new_find_alert_by_id_usecase,
)
from src.domain.alerts.interfaces.alert_repo import AlertRepository
from src.infrastructure.mongodb.alerts.alert_repo import mongo_alert_repository


def get_mongo_alert_repository() -> AlertRepository:
    return mongo_alert_repository()


def get_create_alert_usecase(
    alert_repository: AlertRepository = Depends(get_mongo_alert_repository),
) -> CreateAlertUseCase:
    return new_create_alert_usecase(alert_repository)


def get_find_alert_by_id_usecase(
    alert_repository: AlertRepository = Depends(get_mongo_alert_repository),
) -> FindAlertByIdUseCase:
    return new_find_alert_by_id_usecase(alert_repository)
