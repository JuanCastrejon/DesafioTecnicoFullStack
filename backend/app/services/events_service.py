from datetime import date, datetime, timedelta, timezone

from app.schemas.event import EventDetail, EventListResponse, EventLocation, EventSummary, PaginationMeta


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


def get_event_detail_by_id(event_id: int) -> EventDetail | None:
    event_summary = next((item for item in SEED_EVENTS if item.id == event_id), None)
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
