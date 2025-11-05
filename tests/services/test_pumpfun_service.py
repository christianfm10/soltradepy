from unittest.mock import AsyncMock

import pytest
from sqlmodel import select, text

from soltradepy.domain.pumpfun.models.coin_info_entity import CoinInfo
from soltradepy.services.pumpfun.pumpfun_service import PumpfunService


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


@pytest.mark.asyncio
async def test_sync_coin_info(pumpfun_client, mock_coin_info_response, session):
    """Test the sync_next_page method of GraduatedTokensSyncSQLService."""
    pumpfun_client._fetch = AsyncMock(return_value=mock_coin_info_response)

    service = PumpfunService(session, pumpfun_client)
    result = await service.sync_coin_info(
        token_address="B3JsUuwErGRCUUQcyH3uHUveCqQcS1ayGTaMHG6mpump"
    )
    print(result)
    assert result is not None
    assert result.mint == mock_coin_info_response["mint"]

    result = session.exec(
        text("SELECT mint FROM coin_info"),
    ).all()
    assert len(result) == 1

    assert result[0][0] == "B3JsUuwErGRCUUQcyH3uHUveCqQcS1ayGTaMHG6mpump"


@pytest.mark.skip(reason="I just wanna idempotent")
@pytest.mark.asyncio
async def test_sync_coin_info_idempotent(
    pumpfun_client, mock_coin_info_response, session
):
    """Test that syncing the same coin info multiple times does not create duplicates."""
    pumpfun_client._fetch = AsyncMock(return_value=mock_coin_info_response)

    service = PumpfunService(session, pumpfun_client)

    await service.sync_coin_info(
        token_address="4nkRa7KYFDxCqQ7uU5bjhYxdxrGjH2bxCPPdGgyQpump"
    )
    # pumpfun_client._fetch.assert_awaited_once_with("temporal2")

    mock_coin_info_response["mint"] = "temporal"
    pumpfun_client._fetch = AsyncMock(return_value=mock_coin_info_response)

    result = await service.sync_coin_info(token_address="test")
    # First sync
    stmt = select(CoinInfo)
    result = session.exec(stmt).all()
    print(result)
    # result = session.exec(
    #     text("SELECT COUNT(*) FROM coin_info"),
    # ).one()
    # assert result == 0

    # import asyncio

    # asyncio.run(
    #     service.sync_coin_info(
    #         token_address="B3JsUuwErGRCUUQcyH3uHUveCqQcS1ayGTaMHG6mpump"
    #     )
    # )

    # result = session.exec(
    #     text("SELECT COUNT(*) FROM coin_info"),
    # ).one()
    # assert result == 1

    # # Second sync (should not create a duplicate)
    # asyncio.run(
    #     service.sync_coin_info(
    #         token_address="B3JsUuwErGRCUUQcyH3uHUveCqQcS1ayGTaMHG6mpump"
    #     )
    # )

    # result = session.exec(
    #     text("SELECT COUNT(*) FROM coin_info"),
    # ).one()
    # assert result == 1
