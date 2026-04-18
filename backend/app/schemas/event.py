from datetime import datetime
from pydantic import BaseModel, Field


class EventLocation(BaseModel):
    lat: float = Field(..., examples=[4.711])
    lng: float = Field(..., examples=[-74.072])
    address: str = Field(..., examples=["Parque Simon Bolivar, Bogota"])


class EventDetail(BaseModel):
    id: int
    title: str
    description: str
    date: datetime
    location: EventLocation


class EventSummary(BaseModel):
    id: int
    title: str
    date: datetime


class PaginationMeta(BaseModel):
    page: int
    size: int
    total: int


class EventListResponse(BaseModel):
    data: list[EventSummary]
    meta: PaginationMeta
