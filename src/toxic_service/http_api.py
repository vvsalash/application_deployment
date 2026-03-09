from typing import Annotated, Protocol

from fastapi import FastAPI, Query
from pydantic import BaseModel
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response


class ClassifierProtocol(Protocol):
    def predict(self, text: str) -> bool: ...


class PredictRequest(BaseModel):
    text: str


class PredictResponse(BaseModel):
    is_toxic: bool


HTTP_INFERENCE_COUNTER = Counter(
    "app_http_inference_count",
    "Number of HTTP inference requests",
)


def create_http_app(classifier: ClassifierProtocol) -> FastAPI:
    app = FastAPI(title="Toxic Text Classifier")

    @app.get("/predict", response_model=PredictResponse)
    def predict_get(text: Annotated[str, Query(...)]) -> PredictResponse:
        HTTP_INFERENCE_COUNTER.inc()
        return PredictResponse(is_toxic=classifier.predict(text))

    @app.post("/predict", response_model=PredictResponse)
    def predict_post(payload: PredictRequest) -> PredictResponse:
        HTTP_INFERENCE_COUNTER.inc()
        return PredictResponse(is_toxic=classifier.predict(payload.text))

    @app.get("/metrics")
    def metrics() -> Response:
        return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    return app
