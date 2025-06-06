from abc import ABC, abstractmethod

from src.domain.sensor_events.entities.sensor_event import SensorEvent
from src.domain.sensor_events.value_objects.sensor_event_id import SensorEventId


class SensorEventRepository(ABC):
    @abstractmethod
    async def save(self, sensor_event: SensorEvent) -> None: ...

    @abstractmethod
    async def find_by_id(self, sensor_event_id: SensorEventId) -> SensorEvent | None: ...
