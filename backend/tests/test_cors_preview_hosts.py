from fastapi.testclient import TestClient

from app.main import app


def test_events_should_allow_cors_for_php_client_preview_host() -> None:
    client = TestClient(app)

    response = client.get(
        "/events?page=1&size=1",
        headers={"Origin": "https://php-client-git-develop-juancastrejons-projects.vercel.app"},
    )

    assert response.status_code == 200
    assert (
        response.headers.get("access-control-allow-origin")
        == "https://php-client-git-develop-juancastrejons-projects.vercel.app"
    )


def test_events_should_allow_cors_for_php_client_production_alias() -> None:
    client = TestClient(app)

    response = client.get(
        "/events?page=1&size=1",
        headers={"Origin": "https://php-client-chi.vercel.app"},
    )

    assert response.status_code == 200
    assert response.headers.get("access-control-allow-origin") == "https://php-client-chi.vercel.app"
