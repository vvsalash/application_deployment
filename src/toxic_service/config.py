from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Settings:
    http_host: str = "0.0.0.0"
    http_port: int = 5000
    grpc_host: str = "0.0.0.0"
    grpc_port: int = 50051

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            http_host=os.getenv("HTTP_HOST", "0.0.0.0"),
            http_port=int(os.getenv("HTTP_PORT", "5000")),
            grpc_host=os.getenv("GRPC_HOST", "0.0.0.0"),
            grpc_port=int(os.getenv("GRPC_PORT", "50051")),
        )
