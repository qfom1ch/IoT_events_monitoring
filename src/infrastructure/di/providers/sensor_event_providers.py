from dishka import Provider, Scope, provide

from src.application.use_cases.sensor_event.create_sensor_event_usecase import (
    CreateSensorEventUseCase,
    CreateSensorEventUseCaseImpl,
)
from src.application.use_cases.sensor_event.find_sensor_event_by_id_usecase import (
    FindSensorEventByIdUseCase,
    FindSensorEventByIdUseCaseImpl,
)
from src.domain.sensor_events.interfaces.sensor_event_repo import SensorEventRepository
from src.infrastructure.mongodb.sensor_events.sensor_event_repo import (
    MongoSensorEventRepository,
)


class SensorEventProvider(Provider):
    scope = Scope.REQUEST

    sensor_event_repo = provide(MongoSensorEventRepository, provides=SensorEventRepository)
    create_sensor_event_usecase = provide(
        CreateSensorEventUseCaseImpl, provides=CreateSensorEventUseCase
    )
    find_sensor_event_by_id_usecase = provide(
        FindSensorEventByIdUseCaseImpl, provides=FindSensorEventByIdUseCase
    )
