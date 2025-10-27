import pytest
from soltradepy.services.moralis.graduated_tokens_service import (
    GraduatedTokensSyncJSONService,
)
import soltradepy.storage.graduated_tokens_store as store_module

from sqlmodel import text
from unittest.mock import AsyncMock
from soltradepy.services.moralis.moralis_service import GraduatedTokensSyncSQLService
from soltradepy.storage.cursor_state_store import CursorStateStore
from soltradepy.storage.graduated_tokens_store import GraduatedTokensJSONStore


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
                "graduatedAt": "2025-10-25T08:43:54.000Z",
            },
            # Add more mock token data as needed
        ],
        "pageSize": 5,
        "page": 1,
        "cursor": "mock_cursor_value",
    }


@pytest.mark.asyncio
async def test_sync_next_page__sql(moralis_client, mock_moralis_response, in_memory_db):
    """Test the sync_next_page method of GraduatedTokensSyncSQLService."""
    moralis_client._moralis_request = AsyncMock(return_value=mock_moralis_response)

    graduated_tokens_sync = GraduatedTokensSyncSQLService(moralis_client)
    result = await graduated_tokens_sync.sync_next_page(limit=50)

    assert len(result) == 2
    assert result["next_cursor"] == "mock_cursor_value"

    with store_module.get_session() as session:
        result = session.exec(
            text("SELECT token_address, name FROM graduated_tokens")
        ).all()
    assert len(result) == 1
    assert result[0][0] == "B3JsUuwErGRCUUQcyH3uHUveCqQcS1ayGTaMHG6mpump"


@pytest.mark.asyncio
async def test_sync_next_page__json(moralis_client, mock_moralis_response):
    """Test the sync_next_page method of GraduatedTokensSyncSQLService."""
    moralis_client._moralis_request = AsyncMock(return_value=mock_moralis_response)

    graduated_tokens_sync = GraduatedTokensSyncJSONService(moralis_client)
    result = await graduated_tokens_sync.sync_next_page(limit=50)

    assert len(result) == 2
    assert result["next_cursor"] == "mock_cursor_value"
