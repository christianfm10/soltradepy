# Test for save_sql method in GraduatedTokenRepository
import pytest
from sqlmodel import text

from soltradepy.domain.moralis.models.graduated_token_entity import GraduatedToken
from soltradepy.infrastructure.data_providers.moralis.models.graduated_tokens_response import (
    MoralisGraduatedToken,
)
from soltradepy.storage.graduated_tokens_store import (
    GraduatedTokenRepository,
)


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
    return MoralisGraduatedToken(
        **{
            "token_address": "B3JsUuwErGRCUUQcyH3uHUveCqQcS1ayGTaMHG6mpump",
            "name": "",
            "symbol": "",
            "logo": None,
            "decimals": "6",
            "price_native": "0.000000398",
            "price_usd": "0.000077656",
            "liquidity": "32636.608554306",
            "fully_diluted_valuation": "77656",
            "graduated_at": "2025-10-25T08:43:54.000Z",
        }
    )


@pytest.mark.asyncio
async def test_save_list(fake_graduated_token, session):
    """Test the save_sql method of GraduatedTokensSQLStore."""
    token = GraduatedToken.model_validate(fake_graduated_token)
    token2 = GraduatedToken.model_validate(fake_graduated_token)
    token3 = GraduatedToken.model_validate(fake_graduated_token)

    repository = GraduatedTokenRepository(session)
    repository.save([token, token2])
    repository.save([token3])

    result = session.exec(
        text("SELECT token_address, name FROM graduated_tokens")
    ).all()
    assert len(result) == 1
