from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Any


class MessageConsumer(ABC):
    @abstractmethod
    async def consume(self, topic: str, handler: Callable[[dict[str, Any]], None]) -> None: ...

    @abstractmethod
    async def start(self) -> None: ...

    @abstractmethod
    async def stop(self) -> None: ...
