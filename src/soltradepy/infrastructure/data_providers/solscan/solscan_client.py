from soltradepy.infrastructure.data_providers.base_client import BaseClient
from soltradepy.infrastructure.data_providers.solscan.models.funded_by import (
    FundedByResponse,
)
from soltradepy.infrastructure.data_providers.solscan.models.transfer import (
    TransferResponse,
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

    async def get_transfers(
        self,
        address: str,
        token: str | None = None,
        **kwargs,
    ) -> TransferResponse:
        """
        Get request to Transfer endpoint on solscan.
        **Parameters:**
        - `address` (str): Wallet's Public Key.
        - `token` (str, optional): Token mint address. Exmple: USDC -> "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB"
        - `**kwargs` (dict, optional): Additional query parameters.
            - `page` (int): Number of results to return. Default is 20.
            - `page_size` (int): Number of results to skip. Default is 0.
            - `from_address` (str): Filter by source address.
            - `to` (str): Filter by destination address.
            - `activity_type[]` (list[str]): Filter by activity type.
            - `sort_by` (str): Sort by field. Default is "block_time".
            - `sort_order` (str): Sort order. Default is "desc".
        **Returns**
        - `TransferResponse`: Transfer response from endpoint.
        """
        params = {
            "address": address,
            "remove_spam": "true",
            "exclude_amount_zero": "true",
            "page": 1,
            "page_size": 10,
            "activity_type[]": ["ACTIVITY_SPL_TRANSFER"],
            "token": "So11111111111111111111111111111111111111111",
            "sort_order": "desc",
            "sort_by": "block_time",
            **kwargs,
        }
        if token:
            params["token"] = token

        if "amount" in params:
            params["amount[]"] = params.pop("amount")

        if "from_address" in params:
            params["from"] = params.pop("from_address")

        data = await self._fetch("GET", "/account/transfer", params=params)

        transfers = TransferResponse(**data)

        # return ([Transfer(**tx) for tx in data["data"]], metadata)
        return transfers
