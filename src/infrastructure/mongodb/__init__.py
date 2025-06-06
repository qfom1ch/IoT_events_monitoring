from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from src.core.config import settings
from src.infrastructure.mongodb.alerts.orm import AlertDB
from src.infrastructure.mongodb.devices.orm import DeviceDB
from src.infrastructure.mongodb.sensor_events.orm import SensorEventDB


async def init_mongo() -> None:
    client = AsyncIOMotorClient(settings.MONGO_URI)
    await init_beanie(
        database=client[settings.DATABASE_NAME],
        document_models=[DeviceDB, AlertDB, SensorEventDB],
    )
