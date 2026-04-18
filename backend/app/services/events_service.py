from bisect import bisect_left, bisect_right
from datetime import date, datetime, timedelta, timezone

from app.schemas.event import EventDetail, EventListResponse, EventLocation, EventSummary, PaginationMeta


def _build_seed_events(total: int = 10_000) -> list[EventSummary]:
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
SEED_EVENT_DATES = [item.date.date() for item in SEED_EVENTS]
EVENTS_BY_ID = {item.id: item for item in SEED_EVENTS}


def list_events_paginated(
    page: int,
    size: int,
    from_date: date | None,
    to_date: date | None,
) -> EventListResponse:
    start_index = 0
    end_index = len(SEED_EVENTS)

    if from_date is not None:
        start_index = bisect_left(SEED_EVENT_DATES, from_date)

    if to_date is not None:
        end_index = bisect_right(SEED_EVENT_DATES, to_date)

    if start_index >= end_index:
        return EventListResponse(
            data=[],
            meta=PaginationMeta(page=page, size=size, total=0),
        )

    filtered = SEED_EVENTS[start_index:end_index]
    ordered = list(reversed(filtered))

    total = len(ordered)
    offset = (page - 1) * size
    page_items = ordered[offset : offset + size]

    return EventListResponse(
        data=page_items,
        meta=PaginationMeta(page=page, size=size, total=total),
    )


def get_event_detail_by_id(event_id: int) -> EventDetail | None:
    event_summary = EVENTS_BY_ID.get(event_id)
    if event_summary is None:
        return None

    return EventDetail(
        id=event_summary.id,
        title=event_summary.title,
        description=f"Detalle del {event_summary.title}",
        date=event_summary.date,
        location=EventLocation(
            lat=4.6 + (event_summary.id * 0.001),
            lng=-74.1 - (event_summary.id * 0.001),
            address=f"Direccion evento {event_summary.id}, Bogota",
        ),
    )
