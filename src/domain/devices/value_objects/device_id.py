from dataclasses import dataclass
from uuid import UUID, uuid4


@dataclass(frozen=True)
class DeviceId:
    value: UUID

    @staticmethod
    def generate() -> 'DeviceId':
        return DeviceId(uuid4())

    def __str__(self) -> str:
        return str(self.value)
