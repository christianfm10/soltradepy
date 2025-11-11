from abc import ABC

import httpx


class BaseClient(ABC):
    BASE_URL = "url.com/api"

    def __init__(self, **kwargs):
        self.proxy: str | None = kwargs.get("proxy", None)
        self.clearance: str | None = kwargs.pop("cf_clearance", None)
        self.base_url: str | None = kwargs.pop("base_url", None)
        self.cookies = {}
        if self.base_url is not None:
            self.BASE_URL = self.base_url
        if self.clearance is not None:
            self.cookies["cf_clearance"] = self.clearance
        if self.proxy is not None:
            kwargs["proxy"] = httpx.Proxy(f"http://{self.proxy}")
        self.client = httpx.AsyncClient(cookies=self.cookies, **kwargs)
        self.headers = {"Accept": "application/json"}
        self.client.headers.update(self.headers)

    async def _fetch(
        self,
        method: str,
        endpoint: str = "",
        params: dict | None = None,
        payload: dict | None = None,
    ):
        url = f"{self.BASE_URL}{endpoint}"

        response = await self.client.request(method, url, params=params, json=payload)
        response.raise_for_status()

        return response.json()

    async def _check_ip(self):
        """
        Only for testing purpose
        """
        response = await self.client.get("https://api.ipify.org/?format=json")
        response.raise_for_status()

        print(response.json())
        return response.json()

    async def fake_request(self, address: str):
        """
        Only for testing purpose
        """
        # await asyncio.sleep(5)
        if self.proxy and "bad" in self.proxy:
            # await asyncio.sleep(5)
            raise RuntimeError(f"proxy {self.proxy} fallo")
        return f"resultado de {address} via {self.proxy}"
