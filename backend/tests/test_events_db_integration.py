import os
from datetime import date

import pytest

from app.db.bootstrap import init_events_storage
from app.repositories.events_repository import EventRepository


requires_db = pytest.mark.skipif(
    os.getenv("ENABLE_DB_INTEGRATION_TESTS", "false").lower() != "true",
    reason="Set ENABLE_DB_INTEGRATION_TESTS=true to run PostgreSQL integration tests",
)


event_repository = EventRepository()


@requires_db
def test_db_list_events_should_return_seeded_data() -> None:
    init_events_storage()

    records, total = event_repository.list_events_paginated(
        page=1,
        size=10,
        from_date=None,
        to_date=None,
    )

    assert total >= 10_000
    assert len(records) == 10
    assert [item.id for item in records] == [
        10_000,
        9_999,
        9_998,
        9_997,
        9_996,
        9_995,
        9_994,
        9_993,
        9_992,
        9_991,
    ]


@requires_db
def test_db_list_events_should_filter_by_date_range() -> None:
    init_events_storage()

    records, total = event_repository.list_events_paginated(
        page=1,
        size=10,
        from_date=date(2025, 4, 11),
        to_date=date(2025, 4, 15),
    )

    assert total == 5
    assert [item.id for item in records] == [104, 103, 102, 101, 100]


@requires_db
def test_db_event_detail_should_return_existing_event() -> None:
    init_events_storage()

    detail = event_repository.get_event_by_id(1)

    assert detail is not None
    assert detail.id == 1
    assert detail.title == "Evento 1"
