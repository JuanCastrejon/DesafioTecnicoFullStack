from datetime import date, datetime, timedelta, timezone

from app.schemas.event import EventListResponse, EventSummary, PaginationMeta


def _build_seed_events(total: int = 120) -> list[EventSummary]:
    base = datetime(2025, 1, 1, 8, 0, tzinfo=timezone.utc)
    events: list[EventSummary] = []

    for index in range(1, total + 1):
        events.append(
            EventSummary(
                id=index,
                title=f"Evento {index}",
                date=base + timedelta(days=index),
            )
        )

    return events


SEED_EVENTS = _build_seed_events()


def list_events_paginated(
    page: int,
    size: int,
    from_date: date | None,
    to_date: date | None,
) -> EventListResponse:
    filtered = SEED_EVENTS

    if from_date is not None:
        filtered = [item for item in filtered if item.date.date() >= from_date]

    if to_date is not None:
        filtered = [item for item in filtered if item.date.date() <= to_date]

    ordered = sorted(filtered, key=lambda item: (item.date, item.id), reverse=True)

    total = len(ordered)
    offset = (page - 1) * size
    page_items = ordered[offset : offset + size]

    return EventListResponse(
        data=page_items,
        meta=PaginationMeta(page=page, size=size, total=total),
    )
