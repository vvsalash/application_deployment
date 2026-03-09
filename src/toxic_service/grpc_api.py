from concurrent import futures
from typing import Any, Protocol

import grpc

from toxic_service.grpc_generated import inference_pb2
from toxic_service.grpc_generated import inference_pb2_grpc


class ClassifierProtocol(Protocol):
    def predict(self, text: str) -> bool: ...


class TextClassifierServicer(inference_pb2_grpc.TextClassifierServicer):
    def __init__(self, classifier: ClassifierProtocol) -> None:
        self._classifier = classifier

    def Predict(self, request: Any, context: Any) -> Any:
        result = self._classifier.predict(request.text)
        return inference_pb2.TextClassificationOutput(is_toxic=result)  # type: ignore


def create_grpc_server(classifier: ClassifierProtocol) -> grpc.Server:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    inference_pb2_grpc.add_TextClassifierServicer_to_server(
        TextClassifierServicer(classifier),
        server,
    )
    return server
