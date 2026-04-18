from datetime import date

import pytest
from sqlalchemy.exc import SQLAlchemyError

from app.services import events_service


@pytest.fixture(autouse=True)
def clear_events_cache() -> None:
    events_service.LIST_EVENTS_CACHE.clear()
    events_service.EVENT_DETAIL_CACHE.clear()
    yield
    events_service.LIST_EVENTS_CACHE.clear()
    events_service.EVENT_DETAIL_CACHE.clear()


def test_list_events_should_raise_when_db_fails_and_fallback_disabled(
    monkeypatch,
) -> None:
    monkeypatch.setattr(events_service.settings, "enable_in_memory_fallback", False)

    def raise_db_error(*args, **kwargs):
        raise SQLAlchemyError("db unavailable")

    monkeypatch.setattr(
        events_service.event_repository, "list_events_paginated", raise_db_error
    )

    with pytest.raises(SQLAlchemyError):
        events_service.list_events_paginated(
            page=1, size=10, from_date=None, to_date=None
        )


def test_list_events_should_use_fallback_when_enabled(monkeypatch) -> None:
    monkeypatch.setattr(events_service.settings, "enable_in_memory_fallback", True)

    def raise_db_error(*args, **kwargs):
        raise SQLAlchemyError("db unavailable")

    monkeypatch.setattr(
        events_service.event_repository, "list_events_paginated", raise_db_error
    )

    response = events_service.list_events_paginated(
        page=1,
        size=10,
        from_date=date(2025, 1, 1),
        to_date=date(2025, 1, 20),
    )

    assert response.meta.total == 19
    assert len(response.data) == 10


def test_get_event_detail_should_raise_when_db_fails_and_fallback_disabled(
    monkeypatch,
) -> None:
    monkeypatch.setattr(events_service.settings, "enable_in_memory_fallback", False)

    def raise_db_error(*args, **kwargs):
        raise SQLAlchemyError("db unavailable")

    monkeypatch.setattr(
        events_service.event_repository, "get_event_by_id", raise_db_error
    )

    with pytest.raises(SQLAlchemyError):
        events_service.get_event_detail_by_id(1)
