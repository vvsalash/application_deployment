from toxic_service.config import Settings


def test_settings_defaults(monkeypatch):
    monkeypatch.delenv("HTTP_HOST", raising=False)
    monkeypatch.delenv("HTTP_PORT", raising=False)
    monkeypatch.delenv("GRPC_HOST", raising=False)
    monkeypatch.delenv("GRPC_PORT", raising=False)

    settings = Settings.from_env()

    assert settings.http_host == "0.0.0.0"
    assert settings.http_port == 5000
    assert settings.grpc_host == "0.0.0.0"
    assert settings.grpc_port == 50051


def test_settings_from_env(monkeypatch):
    monkeypatch.setenv("HTTP_HOST", "127.0.0.1")
    monkeypatch.setenv("HTTP_PORT", "8000")
    monkeypatch.setenv("GRPC_HOST", "127.0.0.1")
    monkeypatch.setenv("GRPC_PORT", "6000")

    settings = Settings.from_env()

    assert settings.http_host == "127.0.0.1"
    assert settings.http_port == 8000
    assert settings.grpc_host == "127.0.0.1"
    assert settings.grpc_port == 6000
