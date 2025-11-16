# Test PumpfunClient data provider
from unittest.mock import AsyncMock

import pytest


@pytest.fixture
def mock_coin_info_response():
    """Mock response data for get_coin_info."""
    return {
        "mint": "B3JsUuwErGRCUUQcyH3uHUveCqQcS1ayGTaMHG6mpump",
        "name": "soza business suka ",
        "symbol": "suka",
        "description": "",
        "image_uri": "https://ipfs.io/ipfs/QmVUigtgeFbwrbNHHqPiLFbCa9z16RY4uCDDK2UKtWf6Us",
        "metadata_uri": "https://ipfs.io/ipfs/QmedcZX9S3nkdhyJ3496T4J2hWpFXysAVWkHCQBCjq5TQe",
        "twitter": "https://x.com/i/communities/1981993604928176280",
        "telegram": None,
        "bonding_curve": "EdKEJeCiULLvs3mEwPCbcsccJGHnMNLCjcEuNKc9SLRo",
        "associated_bonding_curve": "3ytsjC2V7zZ2ZZvMaypc58gvhCsGeE2Z5ytSigBEAeB1",
        "creator": "4TR4otqwNY4QomVCJp3gD3HrwSb2H6hUaGiYwHKrpyz5",
        "created_timestamp": 1761379138740,
        "raydium_pool": None,
        "complete": True,
        "virtual_sol_reserves": 115005359823,
        "virtual_token_reserves": 279900000000000,
        "hidden": None,
        "total_supply": 1000000000000000,
        "website": "https://www.tiktok.com/@mellkore?_t=ZS-90q50BNqc6C&_r=1",
        "show_name": True,
        "last_trade_timestamp": 1761381834000,
        "king_of_the_hill_timestamp": 1761380481000,
        "market_cap": 41.76214027360677,
        "nsfw": False,
        "market_id": None,
        "inverted": True,
        "real_sol_reserves": 85005359823,
        "real_token_reserves": 0,
        "livestream_ban_expiry": 0,
        "last_reply": 1761517207000,
        "reply_count": 147,
        "is_banned": False,
        "is_currently_live": False,
        "initialized": True,
        "video_uri": None,
        "updated_at": 1761859944,
        "pump_swap_pool": "9cmTDc4YBd5fbs7M5SCxyiZZ1xaAcSNBTmetBVPRF1ue",
        "ath_market_cap": 94635.71192517118,
        "ath_market_cap_timestamp": 1761480547150,
        "banner_uri": None,
        "hide_banner": False,
        "livestream_downrank_score": 0,
        "program": "pump",
        "platform": None,
        "token_program": None,
        "mayhem_state": None,
        "usd_market_cap": 7634.536863418053,
    }


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
        ]
        * 10,
        "count": 10,
    }


@pytest.mark.asyncio
async def test_get_coin_info(mock_coin_info_response, pumpfun_client):
    """Test fetching coin info from Pump.fun client."""
    pumpfun_client._fetch = AsyncMock(return_value=mock_coin_info_response)
    client_response = await pumpfun_client.get_coin_info(
        token_address="B3JsUuwErGRCUUQcyH3uHUveCqQcS1ayGTaMHG6mpump"
    )

    assert client_response.mint == "B3JsUuwErGRCUUQcyH3uHUveCqQcS1ayGTaMHG6mpump"
    assert client_response.symbol == "suka"


@pytest.mark.asyncio
async def test_get_user_created_coins(mock_user_created_coins_response, pumpfun_client):
    """Test fetching coin info from Pump.fun client."""
    pumpfun_client._fetch = AsyncMock(return_value=mock_user_created_coins_response)
    client_response = await pumpfun_client.get_user_created_coins(
        user_id="4TR4otqwNY4QomVCJp3gD3HrwSb2H6hUaGiYwHKrpyz5", limit=10
    )

    assert client_response.count == 10


@pytest.mark.asyncio
async def test_get_user_token_trades(pumpfun_client):
    """Test fetching developer trades from Pump.fun client."""
    mock_dev_trades_response = {
        "3ppaecEgx9ii6XyjMhux2tUeTLm8FtXnV6UbK4JSTJwP": [
            {
                "slotIndexId": "0003803700650013040000",
                "tx": "2uXRWUftxJoBYDC4phpfvU5cMMkSwE2hpCkvogU5FbbZFdkwAxrULjb4W9D7CqJ6nwbty3WXrqtpJ2Tab89uXvXP",
                "timestamp": "2025-11-16T02:51:10.000Z",
                "userAddress": "3ppaecEgx9ii6XyjMhux2tUeTLm8FtXnV6UbK4JSTJwP",
                "type": "sell",
                "isBondingCurve": True,
                "priceUSD": "0.00002357626546853604368800600075132970576951",
                "priceSOL": "0.0000001680235894399910673383833350120631522198",
                "amountUSD": "1816.25554658824642713891159",
                "amountSOL": "12.944110113",
                "baseAmount": "65507727913762",
                "quoteAmount": "12944110113",
            },
            {
                "slotIndexId": "0003803700160007830002",
                "tx": "3WuHfjNgRZAe4cuLqiU6DHTzaRDFrYfnPsteVFJw3jVEDkne4ddLTsMqUCqpQ8RTr7B9bnhMf9sB7jm7K2CJAREQ",
                "timestamp": "2025-11-16T02:50:51.000Z",
                "userAddress": "3ppaecEgx9ii6XyjMhux2tUeTLm8FtXnV6UbK4JSTJwP",
                "type": "buy",
                "isBondingCurve": True,
                "priceUSD": "0.000004455885890499943249435268277725510269984",
                "priceSOL": "0.00000003171301474684178325316410793850102471019",
                "amountUSD": "274.07447995762482766953526",
                "amountSOL": "1.950617282",
                "baseAmount": "65507727913762",
                "quoteAmount": "1950617282",
            },
        ],
    }
    pumpfun_client._fetch = AsyncMock(return_value=mock_dev_trades_response)
    trades = await pumpfun_client.get_user_token_trades(
        token_address="GThEFKn6HdpEbwAtbAPkhh4zbvJjRo4tG6mb7J4pump",
        user_address="3ppaecEgx9ii6XyjMhux2tUeTLm8FtXnV6UbK4JSTJwP",
    )

    assert len(trades) == 2
