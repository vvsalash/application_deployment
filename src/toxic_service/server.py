import uvicorn

from toxic_service.classifier import ToxicClassifier
from toxic_service.config import Settings
from toxic_service.grpc_api import create_grpc_server
from toxic_service.http_api import create_http_app


def run_http() -> None:
    settings = Settings.from_env()
    classifier = ToxicClassifier()
    app = create_http_app(classifier)
    uvicorn.run(app, host=settings.http_host, port=settings.http_port)


def run_grpc() -> None:
    settings = Settings.from_env()
    classifier = ToxicClassifier()
    server = create_grpc_server(classifier)
    server.add_insecure_port(f"{settings.grpc_host}:{settings.grpc_port}")
    server.start()
    server.wait_for_termination()
