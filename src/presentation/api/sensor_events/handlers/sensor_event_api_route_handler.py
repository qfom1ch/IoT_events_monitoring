from uuid import UUID

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import FastAPI, HTTPException, status

from src.application.use_cases.sensor_event.create_sensor_event_usecase import (
    CreateSensorEventUseCase,
)
from src.application.use_cases.sensor_event.find_sensor_event_by_id_usecase import (
    FindSensorEventByIdUseCase,
)
from src.core.logging_config import setup_logging
from src.domain.sensor_events.exceptions.sensor_event_not_found_error import (
    SensorEventNotFoundError,
)
from src.domain.sensor_events.value_objects.sensor_event_id import SensorEventId
from src.presentation.api.sensor_events.error_messages.sensor_event_not_found_error_message import (  # noqa: E501
    ErrorMessageSensorEventNotFound,
)
from src.presentation.api.sensor_events.schemas.sensor_event_create_schema import (
    SensorEventCreateSchema,
)
from src.presentation.api.sensor_events.schemas.sensor_event_schema import SensorEventSchema
from src.monitoring.metrics import SENSOR_EVENTS_PROCESSED

logger = setup_logging()


class SensorEventApiRouteHandler:
    def register_routes(self, app: FastAPI) -> None:
        @app.get(
            '/sensor_events/{sensor_event_id}',
            response_model=SensorEventSchema,
            status_code=status.HTTP_200_OK,
            responses={status.HTTP_404_NOT_FOUND: {'model': ErrorMessageSensorEventNotFound}},
            tags=['sensor_events'],
        )
        @inject
        async def get_sensor_event(
            sensor_event_id: UUID, usecase: FromDishka[FindSensorEventByIdUseCase]
        ) -> SensorEventSchema:
            uuid = SensorEventId(sensor_event_id)
            try:
                sensor_event = await usecase.execute(uuid)
            except SensorEventNotFoundError as e:
                logger.error(
                    'Sensor event get failed',
                    extra={'extra': {'error': str(e), 'sensor_event_id': sensor_event_id}},
                )
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail=e.message
                ) from e
            except Exception as e:
                logger.error(
                    'Sensor event get failed',
                    extra={'extra': {'error': str(e), 'sensor_event_id': sensor_event_id}},
                )
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR) from e

            logger.info(
                'Sensor event get success', extra={'extra': {'device_id': str(sensor_event.id)}}
            )
            return SensorEventSchema.from_entity(sensor_event)

        @app.post(
            '/sensor_events',
            response_model=SensorEventSchema,
            status_code=status.HTTP_201_CREATED,
            responses={status.HTTP_400_BAD_REQUEST: {}},
            tags=['sensor_events'],
        )
        @inject
        async def create_sensor_event(
            data: SensorEventCreateSchema, usecase: FromDishka[CreateSensorEventUseCase]
        ) -> SensorEventSchema:
            try:
                sensor_event = await usecase.execute(
                    data.device_id, data.sensor_type, data.value, data.metadata
                )
            except Exception as e:
                logger.error(
                    'Sensor event create failed',
                    extra={'extra': {'error': str(e), 'data': data.model_dump_json()}},
                )
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR) from e

            logger.info(
                'Sensor event create success',
                extra={'extra': {'device_id': str(sensor_event.id)}},
            )
            SENSOR_EVENTS_PROCESSED.inc()

            return SensorEventSchema.from_entity(sensor_event)
