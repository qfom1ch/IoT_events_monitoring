from uuid import UUID

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import FastAPI, HTTPException, status

from src.application.use_cases.devices.create_device_usecase import CreateDeviceUseCase
from src.application.use_cases.devices.delete_device_usecase import DeleteDeviceUseCase
from src.application.use_cases.devices.find_device_by_id_usecase import FindDeviceByIdUseCase
from src.application.use_cases.devices.update_device_usecase import UpdateDeviceUseCase
from src.domain.devices.exceptions.device_not_found_error import DeviceNotFoundError
from src.domain.devices.value_objects.device_id import DeviceId
from src.presentation.api.devices.error_messages.device_not_found_error_message import (
    ErrorMessageDeviceNotFound,
)
from src.presentation.api.devices.schemas.device_create_schema import DeviceCreateSchema
from src.presentation.api.devices.schemas.device_schema import DeviceSchema
from src.presentation.api.devices.schemas.device_update_schema import DeviceUpdateSchema


class DeviceApiRouteHandler:
    def register_routes(self, app: FastAPI) -> None:
        @app.get(
            '/devices/{device_id}',
            response_model=DeviceSchema,
            status_code=status.HTTP_200_OK,
            responses={status.HTTP_404_NOT_FOUND: {'model': ErrorMessageDeviceNotFound}},
            tags=['devices'],
        )
        @inject
        async def get_device(
            device_id: UUID, usecase: FromDishka[FindDeviceByIdUseCase]
        ) -> DeviceSchema:
            uuid = DeviceId(device_id)
            try:
                device = await usecase.execute(uuid)
            except DeviceNotFoundError as e:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail=e.message
                ) from e
            except Exception as exc:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR) from exc
            return DeviceSchema.from_entity(device)

        @app.post(
            '/devices',
            response_model=DeviceSchema,
            status_code=status.HTTP_201_CREATED,
            responses={status.HTTP_400_BAD_REQUEST: {}},
            tags=['devices'],
        )
        @inject
        async def create_device(
            data: DeviceCreateSchema, usecase: FromDishka[CreateDeviceUseCase]
        ) -> DeviceSchema:
            try:
                device = await usecase.execute(data.name, data.location, data.sensor_type)
            except Exception as e:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR) from e

            return DeviceSchema.from_entity(device)

        @app.put(
            '/devices/{device_id}',
            response_model=DeviceSchema,
            status_code=status.HTTP_200_OK,
            responses={status.HTTP_404_NOT_FOUND: {'model': ErrorMessageDeviceNotFound}},
            tags=['devices'],
        )
        @inject
        async def update_device(
            device_id: UUID, data: DeviceUpdateSchema, usecase: FromDishka[UpdateDeviceUseCase]
        ) -> DeviceSchema:
            _id = DeviceId(device_id)

            try:
                device = await usecase.execute(_id, data.name, data.location, data.sensor_type)
            except DeviceNotFoundError as e:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail=e.message
                ) from e
            except Exception as e:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR) from e

            return DeviceSchema.from_entity(device)

        @app.delete(
            '/devices/{device_id}',
            status_code=status.HTTP_204_NO_CONTENT,
            responses={status.HTTP_404_NOT_FOUND: {'model': ErrorMessageDeviceNotFound}},
            tags=['devices'],
        )
        @inject
        async def delete_device(
            device_id: UUID, usecase: FromDishka[DeleteDeviceUseCase]
        ) -> None:
            _id = DeviceId(device_id)

            try:
                await usecase.execute(_id)
            except DeviceNotFoundError as e:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail=e.message
                ) from e
            except Exception as e:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR) from e
