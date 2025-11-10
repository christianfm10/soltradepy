from soltradepy.infrastructure.data_providers.base_client import BaseClient
from soltradepy.infrastructure.data_providers.solscan.models.funded_by import (
    FundedByResponse,
)


class SolscanClient(BaseClient):
    BASE_URL = "https://api-v2.solscan.io/v2"

    DEFAULT_HEADERS = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate",
        "Origin": "https://solscan.io",
        "Referer": "https://solscan.io",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
    }

    def __init__(
        self,
        **kwargs,
    ):
        """
        Initialize a Solscan Client instance

        **Parameters:**
        - `**kwargs` (dict, optional): Opciones adicionales.
            - `verify` (bool): Verify SSL.
            - `timeout` (int): Timeout request.
            - `proxy` (str): Proxy address.
            - `cf_clearance` (str): Cloudflare clearance token.

        **Returns:**
        - `SolscanClient`: Solscan Client
        """
        super().__init__(**kwargs)
        self.client.headers.update(self.DEFAULT_HEADERS)

    async def get_funded_by(self, address: str) -> FundedByResponse:
        """
        Get request to FundedBy endpoint on solscan.

        **Parameters:**
        - `address` (str): Wallet's Public Key.
        **Returns**
        - `FundedByResponse`: Funded by response from endpoint.
        """
        endpoint = "/account/funded_by"
        params = {
            "address": address,
        }

        return FundedByResponse(**await self._fetch("GET", endpoint, params))
