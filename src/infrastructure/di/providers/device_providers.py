from dishka import Provider, Scope, provide

from src.application.use_cases.devices.create_device_usecase import (
    CreateDeviceUseCase,
    CreateDeviceUseCaseImpl,
)
from src.application.use_cases.devices.delete_device_usecase import (
    DeleteDeviceUseCase,
    DeleteDeviceUseCaseImpl,
)
from src.application.use_cases.devices.find_device_by_id_usecase import (
    FindDeviceByIdUseCase,
    FindDeviceByIdUseCaseImpl,
)
from src.application.use_cases.devices.update_device_usecase import (
    UpdateDeviceUseCase,
    UpdateDeviceUseCaseImpl,
)
from src.domain.devices.interfaces.device_repo import DeviceRepository
from src.infrastructure.mongodb.devices.device_repo import MongoDeviceRepository


class DeviceProvider(Provider):
    scope = Scope.REQUEST

    device_repo = provide(MongoDeviceRepository, provides=DeviceRepository)
    create_device_usecase = provide(CreateDeviceUseCaseImpl, provides=CreateDeviceUseCase)
    find_device_by_id_usecase = provide(
        FindDeviceByIdUseCaseImpl, provides=FindDeviceByIdUseCase
    )
    update_device_usecase = provide(UpdateDeviceUseCaseImpl, provides=UpdateDeviceUseCase)
    delete_device_usecase = provide(DeleteDeviceUseCaseImpl, provides=DeleteDeviceUseCase)
