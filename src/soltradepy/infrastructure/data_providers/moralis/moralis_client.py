from typing import List
from itertools import cycle

from soltradepy.infrastructure.data_providers.base_client import BaseClient
from soltradepy.infrastructure.data_providers.moralis.models.graduated_tokens_response import (
    MoralisGraduatedTokensResponse,
)


class MoralisClient(BaseClient):
    BASE_URL = "https://solana-gateway.moralis.io"

    def __init__(self, api_keys: List[str]):
        """
        Initialize client with multiple API keys
        Args:
            api_keys: List of Moralis API keys to rotate through
        """
        if not api_keys:
            raise ValueError("At least one API key is required")
            
        super().__init__()
        self.api_keys = api_keys
        self.key_cycle = cycle(api_keys)
        self._update_headers()

    def _update_headers(self) -> None:
        """Update client headers with next API key in rotation"""
        current_key = next(self.key_cycle)
        self.client.headers.update({"X-API-Key": current_key})

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

        # Update headers with next API key before making request
        self._update_headers()

        return MoralisGraduatedTokensResponse(
            **await self._fetch("GET", endpoint, params)
        )
