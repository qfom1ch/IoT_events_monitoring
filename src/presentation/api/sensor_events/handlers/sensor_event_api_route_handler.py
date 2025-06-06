from uuid import UUID

from fastapi import Depends, FastAPI, HTTPException, status

from src.application.use_cases.sensor_event.create_sensor_event_usecase import (
    CreateSensorEventUseCase,
)
from src.application.use_cases.sensor_event.find_sensor_event_by_id_usecase import (
    FindSensorEventByIdUseCase,
)
from src.domain.sensor_events.exceptions.sensor_event_not_found_error import (
    SensorEventNotFoundError,
)
from src.domain.sensor_events.value_objects.sensor_event_id import SensorEventId
from src.infrastructure.di.sensor_event_injection import (
    get_create_sensor_event_usecase,
    get_find_sensor_event_by_id_usecase,
)
from src.presentation.api.sensor_events.error_messages.sensor_event_not_found_error_message import (  # noqa: E501
    ErrorMessageSensorEventNotFound,
)
from src.presentation.api.sensor_events.schemas.sensor_event_create_schema import (
    SensorEventCreateSchema,
)
from src.presentation.api.sensor_events.schemas.sensor_event_schema import SensorEventSchema


class SensorEventApiRouteHandler:
    def register_routes(self, app: FastAPI) -> None:
        @app.get(
            '/sensor_events/{sensor_event_id}',
            response_model=SensorEventSchema,
            status_code=status.HTTP_200_OK,
            responses={status.HTTP_404_NOT_FOUND: {'model': ErrorMessageSensorEventNotFound}},
            tags=['sensor_events'],
        )
        async def get_sensor_event(
            sensor_event_id: UUID,
            usecase: FindSensorEventByIdUseCase = Depends(get_find_sensor_event_by_id_usecase),
        ) -> SensorEventSchema:
            uuid = SensorEventId(sensor_event_id)
            try:
                sensor_event = await usecase.execute(uuid)
            except SensorEventNotFoundError as e:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail=e.message
                ) from e
            except Exception as exc:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR) from exc
            return SensorEventSchema.from_entity(sensor_event)

        @app.post(
            '/sensor_events',
            response_model=SensorEventSchema,
            status_code=status.HTTP_201_CREATED,
            responses={status.HTTP_400_BAD_REQUEST: {}},
            tags=['sensor_events'],
        )
        async def create_sensor_event(
            data: SensorEventCreateSchema,
            usecase: CreateSensorEventUseCase = Depends(get_create_sensor_event_usecase),
        ) -> SensorEventSchema:
            try:
                sensor_event = await usecase.execute(
                    data.device_id, data.sensor_type, data.value, data.metadata
                )
            except ValueError as e:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR) from e

            return SensorEventSchema.from_entity(sensor_event)
