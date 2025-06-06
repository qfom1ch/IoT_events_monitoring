from dataclasses import dataclass
from uuid import UUID, uuid4


@dataclass(frozen=True)
class AlertId:
    value: UUID

    @staticmethod
    def generate() -> 'AlertId':
        return AlertId(uuid4())

    def __str__(self) -> str:
        return str(self.value)
