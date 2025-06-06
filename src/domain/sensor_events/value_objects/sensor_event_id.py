from dataclasses import dataclass
from uuid import UUID, uuid4


@dataclass(frozen=True)
class SensorEventId:
    value: UUID

    @staticmethod
    def generate() -> 'SensorEventId':
        return SensorEventId(uuid4())

    def __str__(self) -> str:
        return str(self.value)
