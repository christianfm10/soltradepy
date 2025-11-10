# Test for save_sql method in UserCreatedCoinRepo
import pytest

from soltradepy.domain.core.models.wallet_entity import UserWallet
from soltradepy.storage.pumpfun.user_created_coins_store import (
    UserWalletRepository,
)


@pytest.fixture
def mock_user_created_coins_response():
    """Mock response data for get_user_created_coins."""
    return {
        "coins": [
            {
                "name": "soza business suka ",
                "symbol": "suka",
                "mint": "B3JsUuwErGRCUUQcyH3uHUveCqQcS1ayGTaMHG6mpump",
                "bonding_curve": "EdKEJeCiULLvs3mEwPCbcsccJGHnMNLCjcEuNKc9SLRo",
            }
        ],
        "count": 1,
    }


@pytest.fixture
def fake_user_created_coins(mock_user_created_coins_response):
    """Create a fake CoinInfoEntity instance."""

    mock_user_created_coins_response["public_key"] = (
        "4TR4otqwNY4QomVCJp3gD3HrwSb2H6hUaGiYwHKrpyz5"
    )
    fake_user_wallet = UserWallet.from_user_created_coins(
        mock_user_created_coins_response
    )

    return fake_user_wallet


@pytest.mark.asyncio
async def test_save(session):
    """Test the save_sql method of UserCreatedCoinInfo"""

    repository = UserWalletRepository(session=session)
    mock_user_created_coins_response = {
        "public_key": "4TR4otqwNY4QomVCJp3gD3HrwSb2H6hUaGiYwHKrpyz5",
        "created_tokens_count": 1,
    }

    user = repository.save(fields=mock_user_created_coins_response)
    assert user is not None
    assert user.public_key == mock_user_created_coins_response["public_key"]
    assert (
        user.created_tokens_count
        == mock_user_created_coins_response["created_tokens_count"]
    )
