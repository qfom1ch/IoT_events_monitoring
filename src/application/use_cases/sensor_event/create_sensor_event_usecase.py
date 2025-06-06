from abc import abstractmethod
from typing import Any
from uuid import UUID

from src.domain.enums import SensorType
from src.domain.sensor_events.entities.sensor_event import SensorEvent
from src.domain.sensor_events.interfaces.sensor_event_repo import SensorEventRepository


class CreateSensorEventUseCase:
    @abstractmethod
    async def execute(
        self,
        device_id: UUID,
        sensor_type: SensorType,
        value: float,
        metadata: dict[str, Any] | None = None,
    ) -> SensorEvent: ...


class CreateSensorEventUseCaseImpl(CreateSensorEventUseCase):
    def __init__(self, repository: SensorEventRepository) -> None:
        self.repository = repository

    async def execute(
        self,
        device_id: UUID,
        sensor_type: SensorType,
        value: float,
        metadata: dict[str, Any] | None = None,
    ) -> SensorEvent:
        sensor_event = SensorEvent.create(
            device_id=device_id, sensor_type=sensor_type, value=value, metadata=metadata or {}
        )
        await self.repository.save(sensor_event)
        return sensor_event


def new_create_sensor_event_usecase(
    sensor_event_repository: SensorEventRepository,
) -> CreateSensorEventUseCase:
    return CreateSensorEventUseCaseImpl(sensor_event_repository)
