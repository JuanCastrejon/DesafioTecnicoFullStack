from datetime import date, datetime, time, timedelta, timezone

from sqlalchemy import func, select

from app.db.session import SessionLocal
from app.models.event import Event


class EventRepository:
    def list_events_paginated(
        self,
        page: int,
        size: int,
        from_date: date | None,
        to_date: date | None,
    ) -> tuple[list[Event], int]:
        filters = []

        if from_date is not None:
            from_dt = datetime.combine(from_date, time.min, tzinfo=timezone.utc)
            filters.append(Event.event_date >= from_dt)

        if to_date is not None:
            to_dt_exclusive = datetime.combine(
                to_date + timedelta(days=1), time.min, tzinfo=timezone.utc
            )
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
                    data_stmt.order_by(Event.event_date.desc(), Event.id.desc())
                    .offset(offset)
                    .limit(size)
                )
                .scalars()
                .all()
            )

        return records, total

    def get_event_by_id(self, event_id: int) -> Event | None:
        with SessionLocal() as db:
            return db.get(Event, event_id)
