from dishka import AsyncContainer, make_async_container

from src.infrastructure.di.providers.alert_providers import AlertProvider
from src.infrastructure.di.providers.cross_providers import CrossProvider
from src.infrastructure.di.providers.device_providers import DeviceProvider
from src.infrastructure.di.providers.sensor_event_providers import SensorEventProvider


def create_container() -> AsyncContainer:
    return make_async_container(
        DeviceProvider(), AlertProvider(), SensorEventProvider(), CrossProvider()
    )
