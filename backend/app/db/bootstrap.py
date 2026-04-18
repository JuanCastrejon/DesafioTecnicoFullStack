import logging
from datetime import datetime, timedelta, timezone

from sqlalchemy import func, select
from sqlalchemy.exc import SQLAlchemyError

from app.core.config import get_settings
from app.db.session import SessionLocal, engine
from app.db.health import ensure_database_ready
from app.models.base import Base
from app.models.event import Event


logger = logging.getLogger(__name__)
settings = get_settings()


def _build_seed_events(total: int = 10_000) -> list[dict[str, object]]:
    base = datetime(2025, 1, 1, 8, 0, tzinfo=timezone.utc)
    events: list[dict[str, object]] = []

    for index in range(1, total + 1):
        events.append(
            {
                "title": f"Evento {index}",
                "description": f"Detalle del Evento {index}",
                "event_date": base + timedelta(days=index),
                "lat": 4.6 + (index * 0.001),
                "lng": -74.1 - (index * 0.001),
                "address": f"Direccion evento {index}, Bogota",
            }
        )

    return events


def init_events_storage() -> None:
    if not settings.run_db_bootstrap:
        logger.info(
            "events storage bootstrap skipped because RUN_DB_BOOTSTRAP is disabled"
        )
        return

    if settings.enable_in_memory_fallback:
        try:
            ensure_database_ready()
        except SQLAlchemyError:
            logger.warning(
                "events storage bootstrap skipped because database is unavailable and fallback is enabled"
            )
            return

    try:
        Base.metadata.create_all(bind=engine)

        with SessionLocal() as db:
            total = db.scalar(select(func.count(Event.id))) or 0
            if total == 0 and settings.seed_events and settings.seed_events_total > 0:
                db.bulk_insert_mappings(
                    Event, _build_seed_events(total=settings.seed_events_total)
                )
                db.commit()
                logger.info(
                    "events storage initialized",
                    extra={"seed_total": settings.seed_events_total},
                )
            elif total == 0 and not settings.seed_events:
                logger.info("events table created without seed data")
    except SQLAlchemyError:
        logger.exception(
            "events storage bootstrap failed",
            extra={"fallback_enabled": settings.enable_in_memory_fallback},
        )
        if not settings.enable_in_memory_fallback:
            raise

        logger.warning(
            "events storage bootstrap skipped because in-memory fallback is enabled"
        )
