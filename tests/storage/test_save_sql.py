# Test for save_sql method in GraduatedTokensSQLStore
from unittest.mock import AsyncMock
import pytest
from sqlmodel import text
from soltradepy.services.moralis.moralis_service import GraduatedTokensSyncSQLService
import soltradepy.storage.graduated_tokens_store as store_module
from soltradepy.storage.cursor_state_store import CursorStateStore
from soltradepy.storage.graduated_tokens_store import GraduatedTokensSQLStore


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


@pytest.fixture
def fake_graduated_token():
    from soltradepy.domain.moralis.models.graduated_token_entity import GraduatedToken

    return GraduatedToken(
        token_address="B3JsUuwErGRCUUQcyH3uHUveCqQcS1ayGTaMHG6mpump",
        name="",
        symbol="",
        logo=None,
        decimals=6,
        price_native=0.000000398,
        price_usd=0.000077656,
        liquidity=32636.608554306,
        fully_diluted_valuation=77656,
        graduated_at="2025-10-25T08:43:54.000Z",
    )


@pytest.mark.asyncio
async def test_save_sql(fake_graduated_token, in_memory_db):
    """Test the save_sql method of GraduatedTokensSQLStore."""
    from soltradepy.domain.moralis.models.graduated_token_entity import GraduatedToken

    token = GraduatedToken.model_validate(fake_graduated_token)
    token2 = GraduatedToken.model_validate(fake_graduated_token)
    token3 = GraduatedToken.model_validate(fake_graduated_token)
    GraduatedTokensSQLStore.save_sql([token, token2])
    GraduatedTokensSQLStore.save_sql([token3])

    with store_module.get_session() as session:
        result = session.exec(
            text("SELECT token_address, name FROM graduated_tokens")
        ).all()
    assert len(result) == 1
    # assert result[0][0] == "B3JsUuwErGRCUUQcyH3uHUveCqQcS1ayGTaMHG6mpump"
