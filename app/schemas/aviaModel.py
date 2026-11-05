from datetime import datetime, timezone
from pydantic import BaseModel, Field
from typing import Literal, Dict


class AviaMetricsBase(BaseModel):
    model: Literal["Airbus A320", "Boeing 737", "SSJ-100", "MS-21", "Другая модель"] = (
        Field(..., description="Модель авиалайнера")
    )
    airline: str = Field(..., description="Авиакомпания")
    altitude: float = Field(..., description="Высота полета")
    speed: float = Field(..., description="Скорость полета")
    latitude: float = Field(..., description="Географическая широта")
    longitude: float = Field(..., description="Географическая долгота")
    linerStatus: Literal["Ожидание взлета", "В полете", "Подготовка"] = Field(
        ..., description="Статус"
    )
    roll: float = Field(0.0, description="Крен судна")
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Время фиксации параметров",
    )


class AviaMetricsCreate(AviaMetricsBase):
    pass


class AviaMetrics(AviaMetricsBase):
    id: int = Field(..., description="Уникальный ID записи")
    links: Dict[str, str] = Field(
        default_factory=dict, description="Гипермедиа ссылки (HATEOAS)"
    )
