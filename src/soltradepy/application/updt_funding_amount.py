import asyncio
import logging

from sqlmodel import text

from soltradepy.infrastructure.data_providers.rpc.constants import HELIUS_RPC
from soltradepy.infrastructure.data_providers.rpc.rpc_client import RPC_Client
from soltradepy.infrastructure.database import get_session

logger = logging.getLogger(__name__)


async def fetch_and_update_funded_amount(session, client: RPC_Client):
    query = """
    SELECT public_key, funded_txn 
    FROM user_wallets 
    WHERE funded_amount IS NULL AND funded_txn IS NOT NULL
    LIMIT 1000;"""
    public_keys = session.execute(text(query)).mappings().all()

    if not public_keys:
        logger.info("No wallets found with missing funded_amount.")
        return
    for row in public_keys:
        public_key = row["public_key"]
        funded_txn = row["funded_txn"]
        logger.info(f"Processing wallet: {public_key}")

        amount = None

        try:
            response = await client.get_transaction(
                signature=funded_txn,
                to_pk=public_key,
            )
            if response.sol_amount is not None:
                amount = response.sol_amount
            logger.info(f"Wallet {public_key} funded amount: {amount}")
        except Exception as e:
            amount = None
            logger.error(f"Error fetching transaction for {public_key}: {e}")

        update_query = """
            UPDATE user_wallets
            SET funded_amount = :amount
            WHERE public_key = :public_key
        """
        session.execute(
            text(update_query),
            {"amount": amount, "public_key": public_key},
        )
        session.commit()


async def main():
    with get_session() as session:
        client = RPC_Client(base_url=HELIUS_RPC)
        await fetch_and_update_funded_amount(session, client)


def cli():
    asyncio.run(main())
