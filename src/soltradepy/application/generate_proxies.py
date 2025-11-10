import logging

from soltradepy.infrastructure.config.env import get_settings
from soltradepy.infrastructure.http.proxy import Host, random_proxies, validate_proxies
from soltradepy.infrastructure.http.store import ProxyStore

# logging with colors, orange for warnings, red for errors, green for info, blue for debug
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logging.getLogger("httpx").setLevel(logging.WARNING)
settings = get_settings()


async def main():
    """Main function to Generate and validate proxies."""
    logging.info("Generating proxies...")
    proxies = random_proxies()
    logging.info(f"{len(proxies)} proxies generated.")
    logging.info(f"Proxies Generated: {proxies}")

    store = ProxyStore()
    logging.info("Loading proxies from store...")
    loaded = store.load()
    logging.info(f"{len(loaded)} proxies loaded from store.")
    logging.info(f"Proxies Loaded: {loaded}")
    store.add_proxies(proxies)
    logging.info("Validating proxies...")
    store._proxies = validate_proxies(store._proxies, timeout=5, host=Host.IPIFY)

    logging.info("Saving proxies to store...")
    store.save()
    logging.info(f"{len(store._proxies)} proxies saved.")
    logging.info(f"Proxies Saved: {store._proxies}")


def cli():
    import asyncio

    asyncio.run(main())
