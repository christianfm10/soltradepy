from soltradepy.infrastructure.data_providers.base_model import APIBaseModel


class Proxy(APIBaseModel):
    host: str
    port: int | None = None
    scheme: str = "http"
    alive: bool = False
    last_checked: str | None = None
    fail_count: int = 0
    # Indicate where the proxy is stored
    store_at: str | None = None

    def __repr__(self) -> str:
        return self.host
