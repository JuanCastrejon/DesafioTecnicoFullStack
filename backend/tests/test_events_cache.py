from datetime import datetime, timezone

from app.models.event import Event
from app.services import events_service
import pytest


@pytest.fixture(autouse=True)
def clear_events_cache() -> None:
    events_service.LIST_EVENTS_CACHE.clear()
    events_service.EVENT_DETAIL_CACHE.clear()
    yield
    events_service.LIST_EVENTS_CACHE.clear()
    events_service.EVENT_DETAIL_CACHE.clear()


def test_list_events_should_use_cache_for_same_query(monkeypatch) -> None:
    calls = {"count": 0}

    def fake_list_from_repository(page: int, size: int, from_date, to_date):
        calls["count"] += 1
        return [], 0

    monkeypatch.setattr(
        events_service.event_repository,
        "list_events_paginated",
        fake_list_from_repository,
    )

    first = events_service.list_events_paginated(
        page=1, size=10, from_date=None, to_date=None
    )
    second = events_service.list_events_paginated(
        page=1, size=10, from_date=None, to_date=None
    )

    assert calls["count"] == 1
    assert first.meta.page == 1
    assert second.meta.page == 1


def test_event_detail_should_use_cache_for_same_id(monkeypatch) -> None:
    calls = {"count": 0}

    def fake_detail_from_repository(event_id: int):
        calls["count"] += 1
        return Event(
            id=event_id,
            title=f"Evento {event_id}",
            description=f"Detalle del Evento {event_id}",
            event_date=datetime(2025, 1, 2, tzinfo=timezone.utc),
            lat=4.7,
            lng=-74.0,
            address="Bogota",
        )

    monkeypatch.setattr(
        events_service.event_repository,
        "get_event_by_id",
        fake_detail_from_repository,
    )

    first = events_service.get_event_detail_by_id(42)
    second = events_service.get_event_detail_by_id(42)

    assert calls["count"] == 1
    assert first is not None
    assert second is not None
    assert first.id == 42
    assert second.id == 42
