from fastapi.testclient import TestClient

from app.api.routes import events as events_route_module
from app import main as app_main
from app.main import app


client = TestClient(app)


def get_error_payload(response):
    payload = response.json()
    assert "code" in payload
    assert "message" in payload
    assert "details" in payload
    assert "request_id" in payload
    assert response.headers["x-request-id"] == payload["request_id"]
    return payload


def test_health_should_return_ok() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_ready_should_return_ok_when_database_is_available(monkeypatch) -> None:
    monkeypatch.setattr(app_main, "ensure_database_ready", lambda: None)

    response = client.get("/ready")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "database": "ready"}


def test_ready_should_return_degraded_when_database_is_unavailable_and_fallback_enabled(
    monkeypatch,
) -> None:
    monkeypatch.setattr(app_main.settings, "enable_in_memory_fallback", True)

    def raise_db_error() -> None:
        raise app_main.SQLAlchemyError("db unavailable")

    monkeypatch.setattr(app_main, "ensure_database_ready", raise_db_error)

    response = client.get("/ready")

    assert response.status_code == 200
    assert response.json() == {
        "status": "degraded",
        "database": "unavailable",
        "fallback": "enabled",
    }


def test_ready_should_return_503_when_database_is_unavailable_and_fallback_disabled(
    monkeypatch,
) -> None:
    monkeypatch.setattr(app_main.settings, "enable_in_memory_fallback", False)

    def raise_db_error() -> None:
        raise app_main.SQLAlchemyError("db unavailable")

    monkeypatch.setattr(app_main, "ensure_database_ready", raise_db_error)

    response = client.get("/ready")

    assert response.status_code == 503
    payload = get_error_payload(response)
    assert payload["code"] == "service_unavailable"
    assert payload["message"] == "database unavailable"


def test_root_should_redirect_to_docs() -> None:
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "/docs"


def test_docs_should_return_custom_swagger_ui() -> None:
    response = client.get("/docs")
    assert response.status_code == 200
    assert "SwaggerUIBundle" in response.text
    assert "theme-toggle" not in response.text
    assert "Filter by tag" not in response.text


def test_list_events_should_return_paginated_results() -> None:
    response = client.get("/events?page=1&size=10")
    assert response.status_code == 200
    payload = response.json()
    assert payload["meta"]["page"] == 1
    assert payload["meta"]["size"] == 10
    assert payload["meta"]["total"] == 10000
    assert len(payload["data"]) == 10
    assert payload["data"][0]["id"] == 10000


def test_list_events_should_return_empty_page_when_offset_exceeds_total() -> None:
    response = client.get("/events?page=1001&size=10")
    assert response.status_code == 200
    payload = response.json()
    assert payload["meta"]["total"] == 10000
    assert payload["data"] == []


def test_list_events_should_filter_by_date_range() -> None:
    response = client.get("/events?from=2025-02-01&to=2025-02-10&page=1&size=50")
    assert response.status_code == 200
    payload = response.json()
    assert payload["meta"]["total"] == 10
    assert len(payload["data"]) == 10


def test_list_events_should_return_400_for_invalid_range() -> None:
    response = client.get("/events?from=2025-03-10&to=2025-03-01")
    assert response.status_code == 400
    payload = get_error_payload(response)
    assert payload["code"] == "bad_request"
    assert payload["message"] == "from must be lower or equal to to"
    assert payload["details"] == "from must be lower or equal to to"


def test_list_events_should_return_422_for_page_size_out_of_range() -> None:
    response = client.get("/events?page=1&size=101")
    assert response.status_code == 422
    payload = get_error_payload(response)
    assert payload["code"] == "validation_error"
    assert isinstance(payload["details"], list)


def test_events_openapi_should_document_date_filter_format() -> None:
    response = client.get("/openapi.json")
    assert response.status_code == 200

    paths = response.json()["paths"]
    list_events_params = paths["/events"]["get"]["parameters"]

    from_param = next(param for param in list_events_params if param["name"] == "from")
    to_param = next(param for param in list_events_params if param["name"] == "to")

    assert "YYYY-MM-DD" in from_param["description"]
    assert "YYYY-MM-DD" in to_param["description"]
    assert "2025-08-01" in str(from_param)
    assert "2025-08-31" in str(to_param)


def test_event_detail_should_return_event() -> None:
    response = client.get("/events/5")
    assert response.status_code == 200
    payload = response.json()
    assert payload["id"] == 5
    assert payload["title"] == "Evento 5"
    assert payload["location"]["address"] == "Direccion evento 5, Bogota"


def test_event_detail_not_found() -> None:
    response_not_found = client.get("/events/10001")
    assert response_not_found.status_code == 404
    payload = get_error_payload(response_not_found)
    assert payload["code"] == "not_found"
    assert payload["message"] == "event not found"


def test_unhandled_exception_should_return_uniform_500_response(monkeypatch) -> None:
    def raise_runtime_error(*args, **kwargs):
        raise RuntimeError("boom")

    monkeypatch.setattr(
        events_route_module, "list_events_paginated", raise_runtime_error
    )

    failing_client = TestClient(app, raise_server_exceptions=False)
    response = failing_client.get("/events?page=1&size=10")

    assert response.status_code == 500
    payload = get_error_payload(response)
    assert payload["code"] == "internal_server_error"
    assert payload["message"] == "Internal server error"
