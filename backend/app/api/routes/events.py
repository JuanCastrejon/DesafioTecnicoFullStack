import logging
from datetime import date

from fastapi import APIRouter, HTTPException, Query

from app.schemas.error import ErrorResponse
from app.schemas.event import EventDetail, EventListResponse
from app.services.events_service import get_event_detail_by_id, list_events_paginated


router = APIRouter(prefix="/events", tags=["events"])
logger = logging.getLogger(__name__)


@router.get(
    "",
    response_model=EventListResponse,
    summary="List Events",
    description=(
        "Retorna eventos paginados. Usa `page` y `size` para la paginación, "
        "y `from` / `to` para filtrar por rango de fechas en formato YYYY-MM-DD."
    ),
    responses={
        400: {"model": ErrorResponse, "description": "Bad request"},
        422: {"model": ErrorResponse, "description": "Validation error"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
    },
)
def list_events(
    page: int = Query(
        1,
        ge=1,
        description="Número de página a consultar, empezando en 1.",
        examples={"default": {"summary": "Primera página", "value": 1}},
    ),
    size: int = Query(
        10,
        ge=1,
        le=100,
        description="Cantidad de eventos por página. Máximo 100.",
        examples={"default": {"summary": "10 elementos por página", "value": 10}},
    ),
    from_date: date | None = Query(
        None,
        alias="from",
        description="Fecha inicial del rango en formato YYYY-MM-DD. No incluir hora.",
        examples={"default": {"summary": "Desde", "value": "2025-08-01"}},
    ),
    to_date: date | None = Query(
        None,
        alias="to",
        description="Fecha final del rango en formato YYYY-MM-DD. No incluir hora.",
        examples={"default": {"summary": "Hasta", "value": "2025-08-31"}},
    ),
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

    return list_events_paginated(
        page=page,
        size=size,
        from_date=from_date,
        to_date=to_date,
    )


@router.get(
    "/{event_id}",
    response_model=EventDetail,
    responses={
        404: {"model": ErrorResponse, "description": "Event not found"},
        422: {"model": ErrorResponse, "description": "Validation error"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
    },
)
def get_event_detail(event_id: int) -> EventDetail:
    logger.info("get_event_detail called", extra={"event_id": event_id})
    event_detail = get_event_detail_by_id(event_id)
    if event_detail is None:
        raise HTTPException(status_code=404, detail="event not found")

    return event_detail
