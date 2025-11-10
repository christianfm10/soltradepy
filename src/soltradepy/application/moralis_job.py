import logging

from soltradepy.infrastructure.config.env import get_settings
from soltradepy.infrastructure.database import get_session
from soltradepy.services.moralis.moralis_service import MoralisService

settings = get_settings()


async def main():
    """Main function to run the Moralis service and get tokens sync job."""

    api_key = settings.moralis_api_key
    session = get_session()
    moralis_service = MoralisService(api_key, session=session)
    logging.info("Starting graduated tokens sync job...")
    result = await moralis_service.sync_graduated_tokens(limit=100)
    logging.info(f"Graduated tokens sync completed: {result}")
    logging.info(f"{result['saved']} tokens graduated was saved")

    # await moralis_service.sync_graduated_tokens()


def cli():
    import asyncio

    asyncio.run(main())


# if __name__ == "__main__":
# asyncio.run(main())
