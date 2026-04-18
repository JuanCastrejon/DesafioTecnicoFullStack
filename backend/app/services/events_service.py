from datetime import date, datetime, timedelta, timezone
import logging

from app.core.config import get_settings
from app.models.event import Event
from app.repositories.events_repository import EventRepository
from app.use_cases.events import (
    EventFallbackData,
    GetEventDetailUseCase,
    ListEventsUseCase,
)
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
FALLBACK_DATA = EventFallbackData.from_events(SEED_EVENTS)

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

LIST_EVENTS_USE_CASE = ListEventsUseCase(
    repository=event_repository,
    cache=LIST_EVENTS_CACHE,
    settings=settings,
    fallback_data=FALLBACK_DATA,
    logger=logger,
)
EVENT_DETAIL_USE_CASE = GetEventDetailUseCase(
    repository=event_repository,
    cache=EVENT_DETAIL_CACHE,
    settings=settings,
    fallback_data=FALLBACK_DATA,
    logger=logger,
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
    return LIST_EVENTS_USE_CASE.execute(
        page=page,
        size=size,
        from_date=from_date,
        to_date=to_date,
    )


def get_event_detail_by_id(event_id: int) -> EventDetail | None:
    return EVENT_DETAIL_USE_CASE.execute(event_id)
