from datetime import datetime, timezone

from sqlalchemy.exc import SQLAlchemyError

from app.core.config import Settings
from app.schemas.event import EventSummary
from app.services.cache import InMemoryTTLCache
from app.use_cases.events import (
    EventFallbackData,
    GetEventDetailUseCase,
    ListEventsUseCase,
)


class FailingEventRepository:
    def list_events_paginated(self, page, size, from_date, to_date):
        raise SQLAlchemyError("database unavailable")

    def get_event_by_id(self, event_id):
        raise SQLAlchemyError("database unavailable")


def test_list_events_use_case_should_fallback_when_database_fails() -> None:
    fallback_events = [
        EventSummary(
            id=1, title="Evento 1", date=datetime(2025, 1, 2, tzinfo=timezone.utc)
        ),
        EventSummary(
            id=2, title="Evento 2", date=datetime(2025, 1, 3, tzinfo=timezone.utc)
        ),
        EventSummary(
            id=3, title="Evento 3", date=datetime(2025, 1, 4, tzinfo=timezone.utc)
        ),
    ]
    fallback_data = EventFallbackData.from_events(fallback_events)
    use_case = ListEventsUseCase(
        repository=FailingEventRepository(),
        cache=InMemoryTTLCache(max_size=16, ttl_seconds=30),
        settings=Settings(enable_in_memory_fallback=True),
        fallback_data=fallback_data,
    )

    response = use_case.execute(page=1, size=2, from_date=None, to_date=None)

    assert response.meta.total == 3
    assert [item.id for item in response.data] == [3, 2]


def test_detail_use_case_should_fallback_when_database_fails() -> None:
    fallback_events = [
        EventSummary(
            id=10, title="Evento 10", date=datetime(2025, 1, 11, tzinfo=timezone.utc)
        ),
        EventSummary(
            id=11, title="Evento 11", date=datetime(2025, 1, 12, tzinfo=timezone.utc)
        ),
    ]
    fallback_data = EventFallbackData.from_events(fallback_events)
    use_case = GetEventDetailUseCase(
        repository=FailingEventRepository(),
        cache=InMemoryTTLCache(max_size=16, ttl_seconds=30),
        settings=Settings(enable_in_memory_fallback=True),
        fallback_data=fallback_data,
    )

    detail = use_case.execute(11)

    assert detail is not None
    assert detail.id == 11
    assert detail.title == "Evento 11"
    assert detail.location.address == "Direccion evento 11, Bogota"
