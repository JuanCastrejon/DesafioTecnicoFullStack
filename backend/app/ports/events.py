from collections.abc import Hashable
from datetime import date
from typing import Protocol, TypeVar

from app.models.event import Event


K = TypeVar("K", bound=Hashable)
V = TypeVar("V")


class CachePort(Protocol[K, V]):
    def get(self, key: K) -> V | None: ...

    def set(self, key: K, value: V) -> None: ...

    def clear(self) -> None: ...


class EventRepositoryPort(Protocol):
    def list_events_paginated(
        self,
        page: int,
        size: int,
        from_date: date | None,
        to_date: date | None,
    ) -> tuple[list[Event], int]: ...

    def get_event_by_id(self, event_id: int) -> Event | None: ...


class FallbackSettingsPort(Protocol):
    enable_in_memory_fallback: bool
