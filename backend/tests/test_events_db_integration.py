import os

import pytest

from app.db.bootstrap import init_events_storage
from app.services.events_service import (
    _get_event_detail_from_db,
    _list_events_paginated_from_db,
)


requires_db = pytest.mark.skipif(
    os.getenv("ENABLE_DB_INTEGRATION_TESTS", "false").lower() != "true",
    reason="Set ENABLE_DB_INTEGRATION_TESTS=true to run PostgreSQL integration tests",
)


@requires_db
def test_db_list_events_should_return_seeded_data() -> None:
    init_events_storage()

    response = _list_events_paginated_from_db(
        page=1,
        size=10,
        from_date=None,
        to_date=None,
    )

    assert response.meta.total >= 10_000
    assert len(response.data) == 10


@requires_db
def test_db_event_detail_should_return_existing_event() -> None:
    init_events_storage()

    detail = _get_event_detail_from_db(1)

    assert detail is not None
    assert detail.id == 1
    assert detail.title == "Evento 1"
