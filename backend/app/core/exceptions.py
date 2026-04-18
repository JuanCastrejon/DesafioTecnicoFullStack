from http import HTTPStatus

from fastapi import HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.logging import request_id_ctx


_CODE_BY_STATUS = {
    HTTPStatus.BAD_REQUEST: "bad_request",
    HTTPStatus.NOT_FOUND: "not_found",
    HTTPStatus.METHOD_NOT_ALLOWED: "method_not_allowed",
    HTTPStatus.UNPROCESSABLE_ENTITY: "validation_error",
    HTTPStatus.SERVICE_UNAVAILABLE: "service_unavailable",
    HTTPStatus.INTERNAL_SERVER_ERROR: "internal_server_error",
}


def _resolve_request_id(request: Request) -> str:
    request_id = getattr(request.state, "request_id", "")
    if request_id:
        return request_id

    return request_id_ctx.get()


def _build_error_payload(
    *, code: str, message: str, request_id: str, details=None
) -> dict[str, object]:
    return {
        "code": code,
        "message": message,
        "details": details,
        "request_id": request_id,
    }


def _build_error_headers(request_id: str) -> dict[str, str]:
    if not request_id:
        return {}

    return {"X-Request-Id": request_id}


def _http_status_code(exception: HTTPException | StarletteHTTPException) -> int:
    return int(getattr(exception, "status_code", HTTPStatus.INTERNAL_SERVER_ERROR))


def _message_from_detail(detail) -> str:
    if isinstance(detail, str):
        return detail
    return "Request could not be processed"


async def http_exception_handler(
    request: Request, exc: HTTPException | StarletteHTTPException
) -> JSONResponse:
    request_id = _resolve_request_id(request)
    status_code = _http_status_code(exc)
    code = _CODE_BY_STATUS.get(HTTPStatus(status_code), "http_error")
    detail = getattr(exc, "detail", None)
    payload = _build_error_payload(
        code=code,
        message=_message_from_detail(detail),
        request_id=request_id,
        details=detail,
    )
    return JSONResponse(
        status_code=status_code,
        content=payload,
        headers=_build_error_headers(request_id),
    )


async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    request_id = _resolve_request_id(request)
    payload = _build_error_payload(
        code="validation_error",
        message="Validation failed",
        request_id=request_id,
        details=exc.errors(),
    )
    return JSONResponse(
        status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
        content=payload,
        headers=_build_error_headers(request_id),
    )


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    request_id = _resolve_request_id(request)
    payload = _build_error_payload(
        code="internal_server_error",
        message="Internal server error",
        request_id=request_id,
        details=None,
    )
    return JSONResponse(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
        content=payload,
        headers=_build_error_headers(request_id),
    )
