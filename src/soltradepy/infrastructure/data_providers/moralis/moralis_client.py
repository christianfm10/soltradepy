# Moralis Solana API Client https://docs.moralis.com/web3-data-api/solana/reference
# Use httpx

import soltradepy.infrastructure.data_providers.moralis.models.graduated_tokens_response as moralis_models


class MoralisClient:
    BASE_URL = "https://solana-gateway.moralis.io"

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {
            "Accept": "application/json",
            "X-API-Key": self.api_key
        }

    async def _moralis_request(self, method: str, endpoint: str, params: dict = None):
        import httpx

        url = f"{self.BASE_URL}{endpoint}"
        async with httpx.AsyncClient() as client:
            response = await client.request(method, url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()

    # cursor param is optional
    async def get_graduated_tokens_by_exchange_pumpfun(self, limit: int = 10, cursor: str = None):
        endpoint = "/token/mainnet/exchange/pumpfun/graduated"
        
        params = {
            "limit": limit,
            **( {"cursor": cursor} if cursor else {} )
        }
        # if cursor:
        #     params["cursor"] = cursor
        return moralis_models.MoralisGraduatedTokensResponse(**await self._moralis_request("GET", endpoint, params))

        return await self._moralis_request("GET", endpoint, params)
