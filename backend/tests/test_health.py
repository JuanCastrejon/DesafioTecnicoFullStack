from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_should_return_ok() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


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


def test_list_events_should_return_422_for_page_size_out_of_range() -> None:
    response = client.get("/events?page=1&size=101")
    assert response.status_code == 422


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
