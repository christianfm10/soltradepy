import asyncio
import logging

from sqlmodel import text

from soltradepy.infrastructure.data_providers.rpc.constants import HELIUS_RPC
from soltradepy.infrastructure.data_providers.rpc.rpc_client import RPC_Client
from soltradepy.infrastructure.database import get_session

logger = logging.getLogger(__name__)

USDC = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"


async def fetch_and_update_has_usdc(session, client: RPC_Client):
    query = "SELECT public_key FROM user_wallets WHERE has_usdc IS NULL;"
    public_keys = session.execute(text(query)).mappings().all()
    # print(public_keys)
    if not public_keys:
        logger.info("No wallets found with missing has_usdc.")
        return
    # return
    for row in public_keys:
        public_key = row["public_key"]
        logger.info(f"Processing wallet: {public_key}")

        has_usdc = False

        try:
            response = await client.get_token_accounts(
                owner=public_key,
                mint=USDC,
                show_zero_balance=True,
            )
            if len(response.token_accounts) > 0:
                has_usdc = True
            logger.info(f"Wallet {public_key} has USDC: {has_usdc}")
        except Exception as e:
            has_usdc = None
            logger.error(f"Error fetching token accounts for {public_key}: {e}")

        update_query = """
            UPDATE user_wallets
            SET has_usdc = :has_usdc
            WHERE public_key = :public_key
        """
        session.execute(
            text(update_query),
            {"has_usdc": has_usdc, "public_key": public_key},
        )
        session.commit()


async def main():
    with get_session() as session:
        client = RPC_Client(base_url=HELIUS_RPC)
        await fetch_and_update_has_usdc(session, client)


def cli():
    asyncio.run(main())
