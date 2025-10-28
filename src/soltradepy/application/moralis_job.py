import logging

from soltradepy.services.moralis.moralis_service import MoralisService
from soltradepy.infrastructure.config.env import settings

# logging with colors, orange for warnings, red for errors, green for info, blue for debug
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


async def main():
    """Main function to run the Moralis service and get tokens sync job."""

    api_key = settings.moralis_api_key
    moralis_service = MoralisService(api_key)
    logging.info("Starting graduated tokens sync job...")
    result = await moralis_service.sync_graduated_tokens(limit=100)
    logging.info(f"Graduated tokens sync completed: {result}")

    # await moralis_service.sync_graduated_tokens()


def cli():
    import asyncio

    asyncio.run(main())


# if __name__ == "__main__":
# asyncio.run(main())
