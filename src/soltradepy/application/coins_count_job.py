import logging

from sqlalchemy import text

from soltradepy.infrastructure.database import get_session
from soltradepy.services.pumpfun.pumpfun_service import PumpfunService

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logging.getLogger("httpx").setLevel(logging.DEBUG)


async def main():
    """Main function to run the sync coins for user wallet method"""
    session = get_session()
    pumpfun_service = PumpfunService(session)
    logging.info("Starting coins for user wallet sync job...")
    stmt = """
    SELECT ci.creator
    FROM coin_info ci
    LEFT JOIN user_wallets uw ON ci.creator = uw.public_key
    WHERE uw.created_tokens_count IS NULL
    """
    wallets = session.scalars(text(stmt)).all()
    for wallet_address in wallets:
        try:
            await pumpfun_service.sync_user_created_coins_for_user_wallet(
                wallet_address=wallet_address,
            )
        except Exception as e:
            logging.error(f"Error saving Wallet {wallet_address}: {e})")
    logging.info(f"Wallet count sync completed: {wallets}")


def cli():
    import asyncio

    asyncio.run(main())
