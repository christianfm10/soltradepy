from soltradepy.infrastructure.data_providers.base_client import BaseClient
from soltradepy.infrastructure.data_providers.moralis.models.graduated_tokens_response import (
    MoralisGraduatedTokensResponse,
)


class MoralisClient(BaseClient):
    BASE_URL = "https://solana-gateway.moralis.io"

    def __init__(self, *, api_key: str, **kwargs):
        """
        Initialize client with multiple API keys
        Args:
            api_keys: List of Moralis API keys to rotate through
        """
        super().__init__(**kwargs)
        self.api_key = api_key
        self.client.headers = {"X-API-Key": self.api_key}

    # cursor param is optional
    async def get_graduated_tokens_by_exchange_pumpfun(
        self, limit: int = 10, cursor: str | None = None
    ) -> MoralisGraduatedTokensResponse:
        """
        Get graduated tokens from Pumpfun exchange
        Args:
            limit: Number of results to return
            cursor: Pagination cursor
        """
        endpoint = "/token/mainnet/exchange/pumpfun/graduated"

        params = {"limit": limit, **({"cursor": cursor} if cursor else {})}

        return MoralisGraduatedTokensResponse(
            **await self._fetch("GET", endpoint, params)
        )
