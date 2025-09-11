from typing import Annotated

from beanie import init_beanie
from dishka import FromDishka, Provider, Scope, provide
from motor.motor_asyncio import AsyncIOMotorClient

from src.core.config import settings, test_settings
from src.infrastructure.mongodb.alerts.orm import AlertDB
from src.infrastructure.mongodb.devices.orm import DeviceDB
from src.infrastructure.mongodb.sensor_events.orm import SensorEventDB


class BeanieInitializer:
    pass


class MongoProvider(Provider):
    scope = Scope.APP

    @provide
    def client(self) -> AsyncIOMotorClient:
        return AsyncIOMotorClient(settings.MONGO_URI)

    @provide
    async def init_beanie(
        self, client: AsyncIOMotorClient
    ) -> Annotated[BeanieInitializer, FromDishka]:
        database = client[settings.DATABASE_NAME]

        await init_beanie(database=database, document_models=[DeviceDB, AlertDB, SensorEventDB])
        return BeanieInitializer()


class TestMongoProvider(MongoProvider):
    @provide
    def client(self) -> AsyncIOMotorClient:
        return AsyncIOMotorClient(test_settings.MONGO_URI)
