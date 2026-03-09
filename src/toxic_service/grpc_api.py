from concurrent import futures
from typing import Any

import grpc

from toxic_service.classifier import ToxicClassifier
from toxic_service.grpc_generated import inference_pb2
from toxic_service.grpc_generated import inference_pb2_grpc


class TextClassifierServicer(inference_pb2_grpc.TextClassifierServicer):
    def __init__(self, classifier: ToxicClassifier) -> None:
        self._classifier = classifier

    def Predict(self, request: Any, context: grpc.ServicerContext) -> Any:
        result = self._classifier.predict(request.text)
        return inference_pb2.TextClassificationOutput(is_toxic=result)  # type: ignore


def create_grpc_server(classifier: ToxicClassifier) -> grpc.Server:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    inference_pb2_grpc.add_TextClassifierServicer_to_server(
        TextClassifierServicer(classifier),
        server,
    )
    return server
