from dishka import AsyncContainer, make_async_container

from src.infrastructure.di.providers.alert_providers import AlertProvider
from src.infrastructure.di.providers.cross_providers import CrossProvider
from src.infrastructure.di.providers.device_providers import DeviceProvider
from src.infrastructure.di.providers.mongo_providers import MongoProvider, TestMongoProvider
from src.infrastructure.di.providers.sensor_event_providers import SensorEventProvider


def create_container() -> AsyncContainer:
    return make_async_container(
        MongoProvider(),
        DeviceProvider(),
        AlertProvider(),
        SensorEventProvider(),
        CrossProvider(),
    )


def create_container_test() -> AsyncContainer:
    return make_async_container(
        TestMongoProvider(),
        DeviceProvider(),
        AlertProvider(),
        SensorEventProvider(),
        CrossProvider(),
    )
