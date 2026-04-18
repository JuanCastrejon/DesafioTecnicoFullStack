from bisect import bisect_left, bisect_right
from datetime import date, datetime, time, timedelta, timezone

from sqlalchemy import func, select
from sqlalchemy.exc import SQLAlchemyError

from app.db.session import SessionLocal
from app.models.event import Event
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


def _to_event_summary(event: Event) -> EventSummary:
    return EventSummary(
        id=event.id,
        title=event.title,
        date=event.event_date,
    )


def _to_event_detail(event: Event) -> EventDetail:
    return EventDetail(
        id=event.id,
        title=event.title,
        description=event.description,
        date=event.event_date,
        location=EventLocation(
            lat=event.lat,
            lng=event.lng,
            address=event.address,
        ),
    )


def _list_events_paginated_from_db(
    page: int,
    size: int,
    from_date: date | None,
    to_date: date | None,
) -> EventListResponse:
    filters = []

    if from_date is not None:
        from_dt = datetime.combine(from_date, time.min, tzinfo=timezone.utc)
        filters.append(Event.event_date >= from_dt)

    if to_date is not None:
        to_dt_exclusive = datetime.combine(to_date + timedelta(days=1), time.min, tzinfo=timezone.utc)
        filters.append(Event.event_date < to_dt_exclusive)

    offset = (page - 1) * size

    with SessionLocal() as db:
        count_stmt = select(func.count(Event.id))
        data_stmt = select(Event)

        if filters:
            count_stmt = count_stmt.where(*filters)
            data_stmt = data_stmt.where(*filters)

        total = db.scalar(count_stmt) or 0

        records = (
            db.execute(
                data_stmt
                .order_by(Event.event_date.desc(), Event.id.desc())
                .offset(offset)
                .limit(size)
            )
            .scalars()
            .all()
        )

    return EventListResponse(
        data=[_to_event_summary(item) for item in records],
        meta=PaginationMeta(page=page, size=size, total=total),
    )


def _get_event_detail_from_db(event_id: int) -> EventDetail | None:
    with SessionLocal() as db:
        event = db.get(Event, event_id)
        if event is None:
            return None

    return _to_event_detail(event)


def list_events_paginated(
    page: int,
    size: int,
    from_date: date | None,
    to_date: date | None,
) -> EventListResponse:
    try:
        return _list_events_paginated_from_db(
            page=page,
            size=size,
            from_date=from_date,
            to_date=to_date,
        )
    except SQLAlchemyError:
        pass

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
    try:
        return _get_event_detail_from_db(event_id)
    except SQLAlchemyError:
        pass

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
