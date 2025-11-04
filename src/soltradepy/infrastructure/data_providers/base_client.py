import httpx


class BaseClient:
    BASE_URL = "url.com/api"

    def __init__(self):
        self.client = httpx.AsyncClient()
        self.headers = {"Accept": "application/json"}
        self.client.headers.update(self.headers)

    async def _fetch(self, method: str, endpoint: str, params: dict | None = None):
        url = f"{self.BASE_URL}{endpoint}"

        response = await self.client.request(method, url, params=params)
        response.raise_for_status()

        return response.json()
