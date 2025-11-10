import logging

from sqlalchemy import text

from soltradepy.infrastructure.database import get_session
from soltradepy.services.pumpfun.pumpfun_service import PumpfunService

# logging with colors, orange for warnings, red for errors, green for info, blue for debug

logging.getLogger("httpx").setLevel(logging.DEBUG)


async def main():
    """Main function to run the Moralis service and get tokens sync job."""
    session = get_session()
    pumpfun_service = PumpfunService(session)
    logging.info("Starting coin info sync job...")
    stmt = """
    SELECT gt.token_address
    FROM graduated_tokens gt
    LEFT JOIN coin_info ci ON gt.token_address = ci.mint
    WHERE ci.mint IS NULL
    """
    tokens = session.scalars(text(stmt)).all()
    for token_address in tokens:
        try:
            await pumpfun_service.sync_coin_info(
                token_address=token_address,
            )
        except Exception as e:
            logging.error(f"Error saving Token {token_address}: {e})")
    logging.info(f"Graduated tokens sync completed: {tokens}")


def cli():
    import asyncio

    asyncio.run(main())
