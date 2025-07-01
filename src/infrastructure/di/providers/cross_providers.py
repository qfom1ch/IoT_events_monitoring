from dishka import Provider, Scope, provide

from src.application.use_cases.cross.process_event_usecase import (
    ProcessEventUseCase,
    ProcessEventUseCaseImpl,
)


class CrossProvider(Provider):
    scope = Scope.REQUEST

    process_event_usecase = provide(ProcessEventUseCaseImpl, provides=ProcessEventUseCase)
