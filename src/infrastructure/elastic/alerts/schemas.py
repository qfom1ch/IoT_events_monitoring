from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, field_validator


class AlertSearchQuery(BaseModel):
    query: str | None = Field(None, description='Поисковый запрос по сообщению алерта')
    device_id: str | None = Field(None, description='ID устройства')
    severity: Literal[1, 2, 3, 4] | None = Field(None, description='Уровень важности')
    min_severity: int | None = Field(
        None, description='Минимальный уровень важности (1-4)', ge=1, le=4
    )
    created_from: datetime | None = Field(None, description='Алерты, созданные c этой даты')
    created_to: datetime | None = Field(None, description='Алерты, созданные до этой даты')
    sort_by: Literal['created_at', 'severity'] | None = Field(
        None, description='Поле для сортировки'
    )
    sort_order: Literal['asc', 'desc'] = Field('desc', description='Направление сортировки')
    page: int = Field(0, ge=0, description='Номер страницы (0-based)')
    size: int = Field(10, ge=1, le=100, description='Размер страницы')

    @field_validator('severity', mode='before')
    def parse_severity(cls, v: str) -> int | None:  # noqa: N805
        if v is None:
            return None
        try:
            num = int(v)
            if num in {1, 2, 3, 4}:
                return num
            raise ValueError()
        except (TypeError, ValueError) as e:
            raise ValueError('severity must be 1, 2, 3 or 4') from e
