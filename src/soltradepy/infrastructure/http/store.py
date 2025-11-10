from collections.abc import Iterable
from datetime import datetime

from soltradepy.infrastructure.http.models import Proxy


class ProxyStore:
    def __init__(self):
        self._proxies: list[Proxy] = []

    def add(self, proxy: Proxy) -> None:
        host = proxy.host
        exists = any(host == p.host for p in self._proxies)
        if not exists:
            self._proxies.append(proxy)

    def add_from_strings(self, proxies: Iterable[str], scheme: str = "http") -> None:
        """
        Añade proxies desde strings: "ip:port" o "ip".
        """
        for proxy in proxies:
            p = Proxy(host=proxy, scheme=scheme, alive=True)
            self.add(p)

    def add_proxies(self, proxies: Iterable[Proxy] | None) -> None:
        if proxies is None:
            return
        for proxy in proxies:
            proxy.store_at = datetime.now().replace(microsecond=0).isoformat()
            self.add(proxy)

    # def check_solscan(self):
    #     proxies = validate_proxies(self._proxies, timeout=5, host=Host.SOLSCAN)
    #     for p in self._proxies
    #     return proxies

    def save(self, path: str = "data/proxies/proxies.json") -> None:
        import json

        data = [p.model_dump() for p in self._proxies]
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def load(self, path: str = "data/proxies/proxies.json") -> list[Proxy]:
        import json

        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
            loaded = [Proxy(**d) for d in data]
            self._proxies = loaded
        except FileNotFoundError as _:
            self._proxies = []
        return self._proxies

    def filter_alive(self) -> list[Proxy]:
        return [p for p in self._proxies if p.alive]
