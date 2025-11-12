import pytest

from soltradepy.infrastructure.data_providers.rpc.constants import HELIUS_RPC
from soltradepy.infrastructure.data_providers.rpc.rpc_client import RPC_Client


@pytest.mark.skip
@pytest.mark.asyncio
async def test_get_token_accounts():
    rpc_client = RPC_Client(base_url=HELIUS_RPC)
    response = await rpc_client.get_token_accounts(
        "DALASbVfzSWnvQ2jmXanU5C3cWPBvM25xmmnBZar72pj",
        show_zero_balance=True,
    )
    assert response.token_accounts is not None


# TODO: Mock get_transaction() response
@pytest.mark.skip
@pytest.mark.asyncio
async def test_get_transaction():
    rpc_client = RPC_Client(base_url=HELIUS_RPC)
    response = await rpc_client.get_transaction(
        signature="3fmy2CEfQjZnGQQtxF3kXLXQJqAi5W2PieCUK9RrzMUZL63g4XNQ399eS6iBxqWevS3hY5g7QXQ33wg8MXeBx8An",
        to_pk="76S6oEPykGMPjnQzXCL3c6Lt86t6cqPby36R4Z99utD",
    )
    # print(response.send_sol_amount)
    # print(response.sol_amount)
    assert response.sol_amount is not None


USDC = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"


# TODO: Mock get_token_accounts response and ensure test does not depend on external service
@pytest.mark.skip
@pytest.mark.asyncio
async def test_has_usdc():
    rpc_client = RPC_Client(base_url=HELIUS_RPC)
    response = await rpc_client.get_token_accounts(
        "BBANfWEPPJnxTeCD3PcxhQ9Z6afaGG4uJNN2Duuhev3H",
        mint=USDC,
        show_zero_balance=True,
    )

    assert len(response.token_accounts) > 0
    assert response.token_accounts is not None
