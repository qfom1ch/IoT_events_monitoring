from abc import ABC, abstractmethod

from src.domain.sensor_events.entities.sensor_event import SensorEvent
from src.domain.sensor_events.exceptions.sensor_event_not_found_error import (
    SensorEventNotFoundError,
)
from src.domain.sensor_events.interfaces.sensor_event_repo import SensorEventRepository
from src.domain.sensor_events.value_objects.sensor_event_id import SensorEventId


class FindSensorEventByIdUseCase(ABC):
    @abstractmethod
    async def execute(self, sensor_event_id: SensorEventId) -> SensorEvent: ...


class FindSensorEventByIdUseCaseImpl(FindSensorEventByIdUseCase):
    def __init__(self, repository: SensorEventRepository) -> None:
        self.repository = repository

    async def execute(self, sensor_event_id: SensorEventId) -> SensorEvent:
        sensor_event: SensorEvent = await self.repository.find_by_id(sensor_event_id)
        if not sensor_event:
            raise SensorEventNotFoundError
        return sensor_event


def new_find_sensor_event_by_id_usecase(
    sensor_event_repository: SensorEventRepository,
) -> FindSensorEventByIdUseCase:
    return FindSensorEventByIdUseCaseImpl(sensor_event_repository)
