import logging
from datetime import datetime

from fastapi import APIRouter, HTTPException, Query

from app.schemas.event import EventDetail, EventListResponse, EventLocation, EventSummary, PaginationMeta


router = APIRouter(prefix="/events", tags=["events"])
logger = logging.getLogger(__name__)


@router.get("", response_model=EventListResponse)
def list_events(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    from_date: datetime | None = Query(None, alias="from"),
    to_date: datetime | None = Query(None, alias="to"),
) -> EventListResponse:
    if from_date and to_date and from_date > to_date:
        raise HTTPException(status_code=400, detail="from must be lower or equal to to")

    logger.info(
        "list_events called",
        extra={
            "page": page,
            "size": size,
            "from": from_date.isoformat() if from_date else None,
            "to": to_date.isoformat() if to_date else None,
        },
    )

    # Placeholder response until DB integration is implemented.
    return EventListResponse(
        data=[],
        meta=PaginationMeta(page=page, size=size, total=0),
    )


@router.get("/{event_id}", response_model=EventDetail)
def get_event_detail(event_id: int) -> EventDetail:
    logger.info("get_event_detail called", extra={"event_id": event_id})
    raise HTTPException(status_code=404, detail="event not found")
