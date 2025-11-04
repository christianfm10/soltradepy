# Test MoralisClient data provider
import pytest
from unittest.mock import AsyncMock


@pytest.fixture
def mock_moralis_response():
    """Mock response data for graduated tokens from Moralis."""
    return {
        "result": [
            {
                "tokenAddress": "B3JsUuwErGRCUUQcyH3uHUveCqQcS1ayGTaMHG6mpump",
                "name": "",
                "symbol": "",
                "logo": None,
                "decimals": "6",
                "priceNative": "0.000000398",
                "priceUsd": "0.000077656",
                "liquidity": "32636.608554306",
                "fullyDilutedValuation": "77656",
                "graduatedAt": "2025-10-25T08:43:54.000Z",
            },
            # Add more mock token data as needed
        ],
        "pageSize": 5,
        "page": 1,
        "cursor": "mock_cursor_value",
    }


@pytest.mark.asyncio
async def test_get_graduated_tokens_by_exchange_pumpfun(
    mock_moralis_response, moralis_client
):
    moralis_client._fetch = AsyncMock(return_value=mock_moralis_response)
    client_response = await moralis_client.get_graduated_tokens_by_exchange_pumpfun(
        limit=5
    )

    client_response = client_response.model_dump()
    assert "result" in client_response
    assert isinstance(client_response["result"], list)
    assert len(client_response["result"]) <= 5
    assert len(client_response["result"]) > 0
