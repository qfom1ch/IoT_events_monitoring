from src.domain.sensor_events.entities.sensor_event import SensorEvent
from src.domain.sensor_events.interfaces.sensor_event_repo import SensorEventRepository
from src.domain.sensor_events.value_objects.sensor_event_id import SensorEventId
from src.infrastructure.mongodb.sensor_events.orm import SensorEventDB


class MongoSensorEventRepository(SensorEventRepository):
    async def find_by_id(self, sensor_event_id: SensorEventId) -> SensorEvent | None:
        if sensor_event_db := await SensorEventDB.get(sensor_event_id.value):
            sensor_event: SensorEvent = sensor_event_db.to_domain()
            return sensor_event
        return None

    async def save(self, sensor_event: SensorEvent) -> None:
        device_db = SensorEventDB.from_domain(sensor_event)
        await device_db.insert()
