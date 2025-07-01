from abc import abstractmethod
from typing import Any
from uuid import UUID

from src.domain.alerts.entities.alert import Alert, AlertSeverity
from src.domain.alerts.interfaces.alert_repo import AlertRepository
from src.domain.devices.exceptions.device_not_found_error import DeviceNotFoundError
from src.domain.devices.interfaces.device_repo import DeviceRepository
from src.domain.devices.value_objects.device_id import DeviceId
from src.domain.enums import SensorType
from src.domain.sensor_events.entities.sensor_event import SensorEvent
from src.domain.sensor_events.interfaces.sensor_event_repo import SensorEventRepository

CRITICAL_TEMPERATURE = 80


class ProcessEventUseCase:
    @abstractmethod
    async def execute(
        self, device_id: UUID, sensor_type: SensorType, value: float, metadata: dict[str, Any]
    ) -> None: ...


class ProcessEventUseCaseImpl(ProcessEventUseCase):
    def __init__(
        self,
        device_repo: DeviceRepository,
        event_repo: SensorEventRepository,
        alert_repo: AlertRepository,
    ) -> None:
        self.device_repo = device_repo
        self.event_repo = event_repo
        self.alert_repo = alert_repo

    async def execute(
        self, device_id: UUID, sensor_type: SensorType, value: float, metadata: dict[str, Any]
    ) -> None:
        device = await self.device_repo.find_by_id(DeviceId(device_id))
        if not device:
            raise DeviceNotFoundError

        sensor_event = SensorEvent.create(
            device_id=device_id, sensor_type=sensor_type, value=value, metadata=metadata
        )
        await self.event_repo.save(sensor_event)

        if sensor_type == SensorType.TEMPERATURE and value > CRITICAL_TEMPERATURE:
            alert = Alert.create(
                event_id=sensor_event.id.value,
                device_id=sensor_event.device_id.value,
                message=f'High temperature: {value}°C',
                severity=AlertSeverity.HIGH,
            )
            await self.alert_repo.save(alert)


def new_process_event_usecase(
    device_repo: DeviceRepository,
    event_repo: SensorEventRepository,
    alert_repo: AlertRepository,
) -> ProcessEventUseCase:
    return ProcessEventUseCaseImpl(device_repo, event_repo, alert_repo)
