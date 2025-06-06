from fastapi import Depends

from src.application.use_cases.devices.create_device_usecase import (
    CreateDeviceUseCase,
    new_create_device_usecase,
)
from src.application.use_cases.devices.delete_device_usecase import (
    DeleteDeviceUseCase,
    new_delete_device_usecase,
)
from src.application.use_cases.devices.find_device_by_id_usecase import (
    FindDeviceByIdUseCase,
    new_find_device_by_id_usecase,
)
from src.application.use_cases.devices.update_device_usecase import (
    UpdateDeviceUseCase,
    new_update_device_usecase,
)
from src.domain.devices.interfaces.device_repo import DeviceRepository
from src.infrastructure.mongodb.devices.device_repo import mongo_device_repository


def get_mongo_device_repository() -> DeviceRepository:
    return mongo_device_repository()


def get_create_device_usecase(
    device_repository: DeviceRepository = Depends(get_mongo_device_repository),
) -> CreateDeviceUseCase:
    return new_create_device_usecase(device_repository)


def get_find_device_by_id_usecase(
    device_repository: DeviceRepository = Depends(get_mongo_device_repository),
) -> FindDeviceByIdUseCase:
    return new_find_device_by_id_usecase(device_repository)


def get_update_device_usecase(
    device_repository: DeviceRepository = Depends(get_mongo_device_repository),
) -> UpdateDeviceUseCase:
    return new_update_device_usecase(device_repository)


def get_delete_device_usecase(
    device_repository: DeviceRepository = Depends(get_mongo_device_repository),
) -> DeleteDeviceUseCase:
    return new_delete_device_usecase(device_repository)
