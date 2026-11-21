import pytest
from fastapi.testclient import TestClient

from app.main import create_app
from app.schemas import AnalyzeResponse


def valid_request() -> dict:
    return {
        "headers": "From: Alice <alice@example.com>\r\nSubject: Hi\r\n",
        "subject": "Hi",
        "body_text": "Hello",
        "body_html": "<p>Hello</p>",
    }


@pytest.fixture
def client() -> TestClient:
    return TestClient(create_app())


def test_health_reports_ok(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_valid_request_returns_a_verdict(client: TestClient) -> None:
    response = client.post("/analyze", json=valid_request())

    assert response.status_code == 200
    AnalyzeResponse.model_validate(response.json())


@pytest.mark.parametrize(
    "request_body",
    [
        pytest.param({**valid_request(), "is_admin": True}, id="unknown-field"),
        pytest.param({**valid_request(), "headers": ""}, id="empty-headers"),
        pytest.param({**valid_request(), "subject": 5}, id="number-instead-of-string"),
    ],
)
def test_invalid_request_is_rejected(client: TestClient, request_body: dict) -> None:
    assert client.post("/analyze", json=request_body).status_code == 422
