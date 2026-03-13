from toxic_service.grpc_api import TextClassifierServicer, create_grpc_server
import inference_pb2


class FakeClassifier:
    def predict(self, text: str) -> bool:
        lowered = text.lower()
        return "idiot" in lowered or "stupid" in lowered


def test_grpc_predict_toxic():
    servicer = TextClassifierServicer(FakeClassifier())
    request = inference_pb2.TextClassificationInput(text="you are stupid idiot")  # type: ignore

    response = servicer.Predict(request, None)

    assert response.is_toxic is True


def test_grpc_predict_clean():
    servicer = TextClassifierServicer(FakeClassifier())
    request = inference_pb2.TextClassificationInput(  # type: ignore
        text="effdl is the best course in the world"
    )

    response = servicer.Predict(request, None)

    assert response.is_toxic is False


def test_create_grpc_server_can_bind_port():
    server = create_grpc_server(FakeClassifier())
    port = server.add_insecure_port("127.0.0.1:0")

    assert isinstance(port, int)
    assert port >= 0
