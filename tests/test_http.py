from fastapi.testclient import TestClient

from toxic_service.http_api import create_http_app


class FakeClassifier:
    def predict(self, text: str) -> bool:
        lowered = text.lower()
        return "idiot" in lowered or "stupid" in lowered


def test_get_predict_clean():
    app = create_http_app(FakeClassifier())
    client = TestClient(app)

    response = client.get("/predict", params={"text": "have a nice day"})
    assert response.status_code == 200
    assert response.json() == {"is_toxic": False}


def test_get_predict_toxic():
    app = create_http_app(FakeClassifier())
    client = TestClient(app)

    response = client.get("/predict", params={"text": "you are an idiot"})
    assert response.status_code == 200
    assert response.json() == {"is_toxic": True}


def test_post_predict():
    app = create_http_app(FakeClassifier())
    client = TestClient(app)

    response = client.post("/predict", json={"text": "you are stupid"})
    assert response.status_code == 200
    assert response.json() == {"is_toxic": True}


def test_health():
    app = create_http_app(FakeClassifier())
    client = TestClient(app)

    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_metrics_endpoint_contains_counter():
    app = create_http_app(FakeClassifier())
    client = TestClient(app)

    client.get("/predict", params={"text": "hello"})
    client.get("/predict", params={"text": "you are an idiot"})

    response = client.get("/metrics")
    assert response.status_code == 200
    assert "app_http_inference_count_total" in response.text
