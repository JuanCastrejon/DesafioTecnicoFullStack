from bisect import bisect_left, bisect_right
from datetime import date, datetime, timedelta, timezone
import logging

from sqlalchemy.exc import SQLAlchemyError

from app.core.config import get_settings
from app.models.event import Event
from app.repositories.events_repository import EventRepository
from app.schemas.event import (
    EventDetail,
    EventListResponse,
    EventLocation,
    EventSummary,
    PaginationMeta,
)
from app.services.cache import InMemoryTTLCache


logger = logging.getLogger(__name__)
settings = get_settings()
event_repository = EventRepository()


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

# Cache dedicado de respuestas frecuentes (bonus):
# - listado: TTL corto para filtros/paginacion repetidos
# - detalle: TTL mayor para lecturas por id
LIST_EVENTS_CACHE = InMemoryTTLCache[
    tuple[int, int, date | None, date | None], EventListResponse
](
    max_size=256,
    ttl_seconds=30,
)
EVENT_DETAIL_CACHE = InMemoryTTLCache[int, EventDetail | None](
    max_size=1024,
    ttl_seconds=60,
)


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
    records, total = event_repository.list_events_paginated(
        page=page,
        size=size,
        from_date=from_date,
        to_date=to_date,
    )

    return EventListResponse(
        data=[_to_event_summary(item) for item in records],
        meta=PaginationMeta(page=page, size=size, total=total),
    )


def _get_event_detail_from_db(event_id: int) -> EventDetail | None:
    event = event_repository.get_event_by_id(event_id)
    if event is None:
        return None

    return _to_event_detail(event)


def list_events_paginated(
    page: int,
    size: int,
    from_date: date | None,
    to_date: date | None,
) -> EventListResponse:
    cache_key = (page, size, from_date, to_date)
    cached_response = LIST_EVENTS_CACHE.get(cache_key)
    if cached_response is not None:
        return cached_response

    try:
        response = _list_events_paginated_from_db(
            page=page,
            size=size,
            from_date=from_date,
            to_date=to_date,
        )
        LIST_EVENTS_CACHE.set(cache_key, response)
        return response
    except SQLAlchemyError:
        logger.exception(
            "list_events database query failed",
            extra={
                "page": page,
                "size": size,
                "from": from_date.isoformat() if from_date else None,
                "to": to_date.isoformat() if to_date else None,
                "fallback_enabled": settings.enable_in_memory_fallback,
            },
        )
        if not settings.enable_in_memory_fallback:
            raise

    logger.warning(
        "list_events using in-memory fallback",
        extra={
            "page": page,
            "size": size,
            "from": from_date.isoformat() if from_date else None,
            "to": to_date.isoformat() if to_date else None,
        },
    )

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

    response = EventListResponse(
        data=page_items,
        meta=PaginationMeta(page=page, size=size, total=total),
    )
    LIST_EVENTS_CACHE.set(cache_key, response)
    return response


def get_event_detail_by_id(event_id: int) -> EventDetail | None:
    cached_detail = EVENT_DETAIL_CACHE.get(event_id)
    if cached_detail is not None:
        return cached_detail

    try:
        detail = _get_event_detail_from_db(event_id)
        if detail is not None:
            EVENT_DETAIL_CACHE.set(event_id, detail)
        return detail
    except SQLAlchemyError:
        logger.exception(
            "get_event_detail database query failed",
            extra={
                "event_id": event_id,
                "fallback_enabled": settings.enable_in_memory_fallback,
            },
        )
        if not settings.enable_in_memory_fallback:
            raise

    logger.warning(
        "get_event_detail using in-memory fallback", extra={"event_id": event_id}
    )

    event_summary = EVENTS_BY_ID.get(event_id)
    if event_summary is None:
        return None

    detail = EventDetail(
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
    EVENT_DETAIL_CACHE.set(event_id, detail)
    return detail
