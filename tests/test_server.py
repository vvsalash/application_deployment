from toxic_service import server


class DummyServer:
    def __init__(self):
        self.bound_address = None
        self.started = False
        self.waited = False

    def add_insecure_port(self, address: str):
        self.bound_address = address

    def start(self):
        self.started = True

    def wait_for_termination(self):
        self.waited = True


def test_run_http(monkeypatch):
    called = {}

    class FakeSettings:
        http_host = "0.0.0.0"
        http_port = 5000

    class FakeClassifier:
        pass

    def fake_from_env():
        return FakeSettings()

    def fake_create_http_app(classifier):
        called["classifier"] = classifier
        return "fake_app"

    def fake_uvicorn_run(app, host, port):
        called["app"] = app
        called["host"] = host
        called["port"] = port

    monkeypatch.setattr(server.Settings, "from_env", staticmethod(fake_from_env))
    monkeypatch.setattr(server, "ToxicClassifier", FakeClassifier)
    monkeypatch.setattr(server, "create_http_app", fake_create_http_app)
    monkeypatch.setattr(server.uvicorn, "run", fake_uvicorn_run)

    server.run_http()

    assert called["app"] == "fake_app"
    assert called["host"] == "0.0.0.0"
    assert called["port"] == 5000


def test_run_grpc(monkeypatch):
    called = {}
    dummy_server = DummyServer()

    class FakeSettings:
        grpc_host = "0.0.0.0"
        grpc_port = 50051

    class FakeClassifier:
        pass

    def fake_from_env():
        return FakeSettings()

    def fake_create_grpc_server(classifier):
        called["classifier"] = classifier
        return dummy_server

    monkeypatch.setattr(server.Settings, "from_env", staticmethod(fake_from_env))
    monkeypatch.setattr(server, "ToxicClassifier", FakeClassifier)
    monkeypatch.setattr(server, "create_grpc_server", fake_create_grpc_server)

    server.run_grpc()

    assert dummy_server.bound_address == "0.0.0.0:50051"
    assert dummy_server.started is True
    assert dummy_server.waited is True
