from uuid import UUID

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import FastAPI, HTTPException, status

from src.application.use_cases.alerts.create_alert_usecase import CreateAlertUseCase
from src.application.use_cases.alerts.find_alert_by_id_usecase import FindAlertByIdUseCase
from src.domain.alerts.exceptions.alert_not_found_error import AlertNotFoundError
from src.domain.alerts.value_objects.alert_id import AlertId
from src.presentation.api.alerts.error_messages.alert_not_found_error_message import (
    ErrorMessageAlertNotFound,
)
from src.presentation.api.alerts.schemas.alert_create_schema import AlertCreateSchema
from src.presentation.api.alerts.schemas.alert_schema import AlertSchema


class AlertApiRouteHandler:
    def register_routes(self, app: FastAPI) -> None:
        @app.get(
            '/alerts/{alert_id}',
            response_model=AlertSchema,
            status_code=status.HTTP_200_OK,
            responses={status.HTTP_404_NOT_FOUND: {'model': ErrorMessageAlertNotFound}},
            tags=['alerts'],
        )
        @inject
        async def get_alert(
            alert_id: UUID, usecase: FromDishka[FindAlertByIdUseCase]
        ) -> AlertSchema:
            uuid = AlertId(alert_id)
            try:
                alert = await usecase.execute(uuid)
            except AlertNotFoundError as e:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail=e.message
                ) from e
            except Exception as exc:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR) from exc
            return AlertSchema.from_entity(alert)

        @app.post(
            '/alerts',
            response_model=AlertSchema,
            status_code=status.HTTP_201_CREATED,
            responses={status.HTTP_400_BAD_REQUEST: {}},
            tags=['alerts'],
        )
        @inject
        async def create_alert(
            data: AlertCreateSchema, usecase: FromDishka[CreateAlertUseCase]
        ) -> AlertSchema:
            try:
                alert = await usecase.execute(
                    data.event_id, data.device_id, data.message, data.severity
                )
            except Exception as e:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR) from e

            return AlertSchema.from_entity(alert)
