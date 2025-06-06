from src.domain.devices.entities.device import Device
from src.domain.devices.interfaces.device_repo import DeviceRepository
from src.domain.devices.value_objects.device_id import DeviceId
from src.infrastructure.mongodb.devices.orm import DeviceDB


class MongoDeviceRepository(DeviceRepository):
    async def find_by_id(self, device_id: DeviceId) -> Device | None:
        if device_db := await DeviceDB.get(device_id.value):
            device: Device = device_db.to_domain()
            return device
        return None

    async def save(self, device: Device) -> None:
        device_db = DeviceDB.from_domain(device)
        await device_db.insert()

    async def update(self, device: Device) -> None:
        device_db = await DeviceDB.get(device.id.value)
        if device_db:
            device_db.name = device.name
            device_db.sensor_type = device.sensor_type.value
            device_db.location = device.location
            device_db.is_active = device.is_active
            await device_db.save()

    async def delete(self, device_id: DeviceId) -> None:
        device_db = await DeviceDB.get(device_id.value)
        if device_db:
            await device_db.delete()


def mongo_device_repository() -> DeviceRepository:
    return MongoDeviceRepository()
