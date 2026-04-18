from collections import OrderedDict
from threading import Lock
from time import monotonic
from typing import Generic, Hashable, TypeVar

K = TypeVar("K", bound=Hashable)
V = TypeVar("V")


class InMemoryTTLCache(Generic[K, V]):
    def __init__(self, max_size: int, ttl_seconds: int) -> None:
        if max_size <= 0:
            raise ValueError("max_size must be > 0")
        if ttl_seconds <= 0:
            raise ValueError("ttl_seconds must be > 0")

        self._max_size = max_size
        self._ttl_seconds = ttl_seconds
        self._store: OrderedDict[K, tuple[float, V]] = OrderedDict()
        self._lock = Lock()

    def get(self, key: K) -> V | None:
        now = monotonic()

        with self._lock:
            entry = self._store.get(key)
            if entry is None:
                return None

            expires_at, value = entry
            if now >= expires_at:
                self._store.pop(key, None)
                return None

            self._store.move_to_end(key)
            return value

    def set(self, key: K, value: V) -> None:
        expires_at = monotonic() + self._ttl_seconds

        with self._lock:
            if key in self._store:
                self._store.pop(key, None)

            self._store[key] = (expires_at, value)
            self._store.move_to_end(key)

            while len(self._store) > self._max_size:
                self._store.popitem(last=False)

    def clear(self) -> None:
        with self._lock:
            self._store.clear()
