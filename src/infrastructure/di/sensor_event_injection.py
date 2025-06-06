from fastapi import Depends

from src.application.use_cases.sensor_event.create_sensor_event_usecase import (
    CreateSensorEventUseCase,
    new_create_sensor_event_usecase,
)
from src.application.use_cases.sensor_event.find_sensor_event_by_id_usecase import (
    FindSensorEventByIdUseCase,
    new_find_sensor_event_by_id_usecase,
)
from src.domain.sensor_events.interfaces.sensor_event_repo import SensorEventRepository
from src.infrastructure.mongodb.sensor_events.sensor_event_repo import (
    mongo_sensor_event_repository,
)


def get_mongo_sensor_event_repository() -> SensorEventRepository:
    return mongo_sensor_event_repository()


def get_create_sensor_event_usecase(
    sensor_event_repository: SensorEventRepository = Depends(get_mongo_sensor_event_repository),
) -> CreateSensorEventUseCase:
    return new_create_sensor_event_usecase(sensor_event_repository)


def get_find_sensor_event_by_id_usecase(
    sensor_event_repository: SensorEventRepository = Depends(get_mongo_sensor_event_repository),
) -> FindSensorEventByIdUseCase:
    return new_find_sensor_event_by_id_usecase(sensor_event_repository)
