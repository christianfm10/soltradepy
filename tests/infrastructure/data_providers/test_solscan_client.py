from unittest.mock import AsyncMock

import pytest

from soltradepy.infrastructure.data_providers.solscan.solscan_client import (
    SolscanClient,
)


@pytest.fixture
def mock_funded_by_response():
    return {
        "data": {
            "address": "DALASbVfzSWnvQ2jmXanU5C3cWPBvM25xmmnBZar72pj",
            "block_time": 1724553042,
            "funded_by": "5VCwKtCXgCJ6kit5FybXjvriW3xELsFDhYrPSqtJNmcD",
            "tx_hash": "5mnFpskAsuwcfSqkMD5GuUUsbBLFpZYbcoaxxB2QcP6E3e6Qnc1NVQvBJtK4UYJbBpxsRuAokFZgPNHetRwqJk5k",
            "cex": "",
            "dex": "",
        },
        "metadata": {
            "accounts": {
                "5VCwKtCXgCJ6kit5FybXjvriW3xELsFDhYrPSqtJNmcD": {
                    "account_address": "5VCwKtCXgCJ6kit5FybXjvriW3xELsFDhYrPSqtJNmcD",
                    "account_icon": "https://statics.solscan.io/solscan-img/okx.png",
                    "account_label": "OKX",
                    "account_tags": ["exchange_wallet"],
                    "account_type": "address",
                }
            },
            "tags": {
                "exchange_wallet": {
                    "tag_id": "exchange_wallet",
                    "tag_name": "Exchange Wallet",
                    "tag_type": 1,
                    "tag_metadata": "",
                }
            },
            "tokens": {
                "So11111111111111111111111111111111111111112": {
                    "token_address": "So11111111111111111111111111111111111111112",
                    "token_name": "Wrapped SOL",
                    "token_symbol": "WSOL",
                    "token_icon": "https://raw.githubusercontent.com/solana-labs/token-list/main/assets/mainnet/So11111111111111111111111111111111111111112/logo.png",
                    "token_decimals": 9,
                    "token_type": "token",
                    "price_usdt": 161.27320403119128,
                    "reputation": "ok",
                    "is_show_value": True,
                    "is_calculate_on_portfolio": True,
                    "is_show_icon": True,
                    "d_source": "r",
                    "token_icon_alternative": None,
                },
                "So11111111111111111111111111111111111111111": {
                    "token_address": "So11111111111111111111111111111111111111111",
                    "token_decimals": 9,
                    "token_name": "SOL",
                    "token_symbol": "SOL",
                    "token_type": "token",
                    "token_icon": "https://statics.solscan.io/solscan-img/solana_icon.svg",
                    "price_usdt": 161.27320403119128,
                    "reputation": "ok",
                    "is_show_value": True,
                    "is_calculate_on_portfolio": True,
                    "is_show_icon": True,
                },
            },
            "nftCollections": {},
            "nftMarketplaces": {},
            "programs": {},
        },
        "success": True,
    }


@pytest.fixture
def solscan_client() -> SolscanClient:
    proxy = "41.89.56.116:3128"  # TODO: Generate random proxy
    return SolscanClient()


@pytest.mark.asyncio
async def test_get_funded_by(solscan_client: SolscanClient, mock_funded_by_response):
    """
    Test get_funded_by request
    """
    solscan_client._fetch = AsyncMock(return_value=mock_funded_by_response)

    response = await solscan_client.get_funded_by(
        address="DALASbVfzSWnvQ2jmXanU5C3cWPBvM25xmmnBZar72pj"
    )

    assert response.success


USDC = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"


# TODO: Mock get_transfers response
@pytest.mark.skip
@pytest.mark.asyncio
async def test_get_transfers(solscan_client: SolscanClient, mock_funded_by_response):
    """
    Test get_transfers request
    """
    # solscan_client._fetch = AsyncMock(return_value=mock_funded_by_response)
    response = await solscan_client.get_transfers(
        address="G6fC9JUeEJxhmX1AGxd9uWBNcZmym9vPrNn72rByydaH",
        token=USDC,
        to="21wG4F3ZR8gwGC47CkpD6ySBUgH9AABtYMBWFiYdTTgv",
    )
    print(len(response.data))

    assert response.success
