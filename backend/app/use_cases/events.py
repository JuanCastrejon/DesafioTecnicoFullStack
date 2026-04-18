from __future__ import annotations

from bisect import bisect_left, bisect_right
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import date
import logging

from sqlalchemy.exc import SQLAlchemyError

from app.core.config import Settings
from app.models.event import Event
from app.ports.events import CachePort, EventRepositoryPort
from app.schemas.event import (
    EventDetail,
    EventListResponse,
    EventLocation,
    EventSummary,
    PaginationMeta,
)


@dataclass(frozen=True)
class EventFallbackData:
    events: tuple[EventSummary, ...]
    dates: tuple[date, ...]
    by_id: Mapping[int, EventSummary]

    @classmethod
    def from_events(cls, events: Sequence[EventSummary]) -> EventFallbackData:
        ordered_events = tuple(sorted(events, key=lambda item: (item.date, item.id)))
        return cls(
            events=ordered_events,
            dates=tuple(item.date.date() for item in ordered_events),
            by_id={item.id: item for item in ordered_events},
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


class ListEventsUseCase:
    def __init__(
        self,
        repository: EventRepositoryPort,
        cache: CachePort[tuple[int, int, date | None, date | None], EventListResponse],
        settings: Settings,
        fallback_data: EventFallbackData,
        logger: logging.Logger | None = None,
    ) -> None:
        self._repository = repository
        self._cache = cache
        self._settings = settings
        self._fallback_data = fallback_data
        self._logger = logger or logging.getLogger(__name__)

    def execute(
        self,
        page: int,
        size: int,
        from_date: date | None,
        to_date: date | None,
    ) -> EventListResponse:
        cache_key = (page, size, from_date, to_date)
        cached_response = self._cache.get(cache_key)
        if cached_response is not None:
            return cached_response

        try:
            records, total = self._repository.list_events_paginated(
                page=page,
                size=size,
                from_date=from_date,
                to_date=to_date,
            )
            response = EventListResponse(
                data=[_to_event_summary(item) for item in records],
                meta=PaginationMeta(page=page, size=size, total=total),
            )
            self._cache.set(cache_key, response)
            return response
        except SQLAlchemyError:
            self._logger.exception(
                "list_events database query failed",
                extra={
                    "page": page,
                    "size": size,
                    "from": from_date.isoformat() if from_date else None,
                    "to": to_date.isoformat() if to_date else None,
                    "fallback_enabled": self._settings.enable_in_memory_fallback,
                },
            )
            if not self._settings.enable_in_memory_fallback:
                raise

        self._logger.warning(
            "list_events using in-memory fallback",
            extra={
                "page": page,
                "size": size,
                "from": from_date.isoformat() if from_date else None,
                "to": to_date.isoformat() if to_date else None,
            },
        )

        start_index = 0
        end_index = len(self._fallback_data.events)

        if from_date is not None:
            start_index = bisect_left(self._fallback_data.dates, from_date)

        if to_date is not None:
            end_index = bisect_right(self._fallback_data.dates, to_date)

        if start_index >= end_index:
            response = EventListResponse(
                data=[],
                meta=PaginationMeta(page=page, size=size, total=0),
            )
            self._cache.set(cache_key, response)
            return response

        filtered = self._fallback_data.events[start_index:end_index]
        ordered = list(reversed(filtered))

        total = len(ordered)
        offset = (page - 1) * size
        page_items = ordered[offset : offset + size]

        response = EventListResponse(
            data=page_items,
            meta=PaginationMeta(page=page, size=size, total=total),
        )
        self._cache.set(cache_key, response)
        return response


class GetEventDetailUseCase:
    def __init__(
        self,
        repository: EventRepositoryPort,
        cache: CachePort[int, EventDetail | None],
        settings: Settings,
        fallback_data: EventFallbackData,
        logger: logging.Logger | None = None,
    ) -> None:
        self._repository = repository
        self._cache = cache
        self._settings = settings
        self._fallback_data = fallback_data
        self._logger = logger or logging.getLogger(__name__)

    def execute(self, event_id: int) -> EventDetail | None:
        cached_detail = self._cache.get(event_id)
        if cached_detail is not None:
            return cached_detail

        try:
            event = self._repository.get_event_by_id(event_id)
            if event is None:
                return None

            detail = _to_event_detail(event)
            self._cache.set(event_id, detail)
            return detail
        except SQLAlchemyError:
            self._logger.exception(
                "get_event_detail database query failed",
                extra={
                    "event_id": event_id,
                    "fallback_enabled": self._settings.enable_in_memory_fallback,
                },
            )
            if not self._settings.enable_in_memory_fallback:
                raise

        self._logger.warning(
            "get_event_detail using in-memory fallback",
            extra={"event_id": event_id},
        )

        event_summary = self._fallback_data.by_id.get(event_id)
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
        self._cache.set(event_id, detail)
        return detail
