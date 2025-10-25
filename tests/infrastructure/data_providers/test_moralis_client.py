# Test MoralisClient data provider
import pytest
import asyncio
from unittest.mock import AsyncMock, patch
from soltradepy.infrastructure.data_providers.moralis.moralis_client import MoralisClient
# {'result': [{'tokenAddress': 'B3JsUuwErGRCUUQcyH3uHUveCqQcS1ayGTaMHG6mpump', 'name': '', 'symbol': '', 'logo': None, 'decimals': '6', 'priceNative': '0.000000398', 'priceUsd': '0.000077656', 'liquidity': '32636.608554306', 'fullyDilutedValuation': '77656', 'graduatedAt': '2025-10-25T08:43:54.000Z'}, {'tokenAddress': '8g5LuAXiLiHhZit9aQiBHpA98ABB8727MRAS6LtCpump', 'name': 'SOLANAHYPER', 'symbol': 'SOLHYPE', 'logo': 'https://logo.moralis.io/solana-mainnet_8g5LuAXiLiHhZit9aQiBHpA98ABB8727MRAS6LtCpump_4ac819e62677953eeea91888c85ba43b.webp', 'decimals': '6', 'priceNative': '0.000000402', 'priceUsd': '0.000078331', 'liquidity': '32780.53122128', 'fullyDilutedValuation': '78331', 'graduatedAt': '2025-10-25T06:30:45.000Z'}, {'tokenAddress': 'Wkef26m8MQSkVTRQsnyoU8H6qUw1hUNGxsRaRxr31XP', 'name': 'ATHENIUM', 'symbol': 'ATHENIUM', 'logo': 'https://logo.moralis.io/solana-mainnet_Wkef26m8MQSkVTRQsnyoU8H6qUw1hUNGxsRaRxr31XP_7518065eb3115d0dacc3ff5dd9ccd494.gif', 'decimals': '6', 'priceNative': '0.0000000187865', 'priceUsd': '0.000003657', 'liquidity': '7080.120685828', 'fullyDilutedValuation': '3657', 'graduatedAt': '2025-10-25T06:23:45.000Z'}, {'tokenAddress': '9Eufcq8yqukb4A9eUTAXrRpzB7aKTdAuUnqe75ttpump', 'name': 'Pumpkin', 'symbol': 'Pumpkin', 'logo': 'https://logo.moralis.io/solana-mainnet_9Eufcq8yqukb4A9eUTAXrRpzB7aKTdAuUnqe75ttpump_e58412a1ec96fe1d9d9563e0e8388d89.webp', 'decimals': '6', 'priceNative': '0.000001311', 'priceUsd': '0.000255377', 'liquidity': '61648.289542736', 'fullyDilutedValuation': '255377', 'graduatedAt': '2025-10-25T06:06:37.000Z'}, {'tokenAddress': 'CaFtnMpi7q6YBenfCaYvF2xhLWdZoDLMx29R2Y7jpump', 'name': "Jayden's bus is here", 'symbol': 'BUS', 'logo': 'https://logo.moralis.io/solana-mainnet_CaFtnMpi7q6YBenfCaYvF2xhLWdZoDLMx29R2Y7jpump_6eb884f9740c759bd9d9540cdef311bb.webp', 'decimals': '6', 'priceNative': '0.000000282', 'priceUsd': '0.000055046', 'liquidity': '27558.842893284', 'fullyDilutedValuation': '54973.36458177720248', 'graduatedAt': '2025-10-25T05:48:11.000Z'}], 'pageSize': 5, 'page': 1, 'cursor': 'eyJhbGciOiJIUzI1NiJ9.eyJwYWdlIjoxLCJmcm9tTG9va3VwIjp7InRva2VuQWRkcmVzcyI6IkNhRnRuTXBpN3E2WUJlbmZDYVl2RjJ4aExXZFpvRExNeDI5UjJZN2pwdW1wIiwiY2F0ZWdvcnkiOiJwdW1wZnVuOmdyYWR1YXRlZCIsImNhdGVnb3J5S2V5IjoxNzYxMzcxMjkxfX0.s8Vudth4BFlcJGO4weXwamrrLKfUW9BsvBD10rTkM3s'}
# Mock data for testing

@pytest.fixture
def moralis_client():
    api_key = "test_api_key"
    return MoralisClient(api_key)   

@pytest.fixture
def mock_moralis_response():
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
                "graduatedAt": "2025-10-25T08:43:54.000Z"
            },
            # Add more mock token data as needed
        ],
        "pageSize": 5,
        "page": 1,
        "cursor": "mock_cursor_value"
    }

@pytest.mark.asyncio
async def test_get_graduated_tokens_by_exchange_pumpfun(mock_moralis_response):
    api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJub25jZSI6Ijc5MmQ3OWU1LTA4MjgtNGE3MS04M2M4LTU5ZWZlNGE0ZDlhMCIsIm9yZ0lkIjoiNDM3NzE0IiwidXNlcklkIjoiNDUwMzAyIiwidHlwZUlkIjoiYzZmODM4N2EtYTk4OC00YmVhLThhOWYtYjYyNTI3YWNjMGYyIiwidHlwZSI6IlBST0pFQ1QiLCJpYXQiOjE3NDI3Mzk1MDksImV4cCI6NDg5ODQ5OTUwOX0.ohloCv08bYJrHBPQORGfH_DgnMbFua_TaA9PG7uINj4"  # Replace with a valid Moralis API key for real testing
    client = MoralisClient(api_key) 
    client._moralis_request = AsyncMock(return_value=mock_moralis_response)
    client_response = await client.get_graduated_tokens_by_exchange_pumpfun(limit=5) 
    print(client_response)

    client_response = client_response.model_dump()
    assert "result" in client_response
    assert isinstance(client_response["result"], list)
    assert len(client_response["result"]) <= 5  