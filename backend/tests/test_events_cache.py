from app.schemas.event import EventDetail, EventListResponse, EventLocation, PaginationMeta
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

    def fake_from_db(page: int, size: int, from_date, to_date) -> EventListResponse:
        calls["count"] += 1
        return EventListResponse(data=[], meta=PaginationMeta(page=page, size=size, total=0))

    monkeypatch.setattr(events_service, "_list_events_paginated_from_db", fake_from_db)

    first = events_service.list_events_paginated(page=1, size=10, from_date=None, to_date=None)
    second = events_service.list_events_paginated(page=1, size=10, from_date=None, to_date=None)

    assert calls["count"] == 1
    assert first.meta.page == 1
    assert second.meta.page == 1


def test_event_detail_should_use_cache_for_same_id(monkeypatch) -> None:
    calls = {"count": 0}

    def fake_detail_from_db(event_id: int) -> EventDetail:
        calls["count"] += 1
        return EventDetail(
            id=event_id,
            title=f"Evento {event_id}",
            description=f"Detalle del Evento {event_id}",
            date=events_service.SEED_EVENTS[0].date,
            location=EventLocation(lat=4.7, lng=-74.0, address="Bogota"),
        )

    monkeypatch.setattr(events_service, "_get_event_detail_from_db", fake_detail_from_db)

    first = events_service.get_event_detail_by_id(42)
    second = events_service.get_event_detail_by_id(42)

    assert calls["count"] == 1
    assert first is not None
    assert second is not None
    assert first.id == 42
    assert second.id == 42
