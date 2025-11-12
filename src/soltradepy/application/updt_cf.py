import asyncio
import logging

from soltradepy.infrastructure.browser.cloudflare_bypass import CloudflareBypass
from soltradepy.infrastructure.http.store import ProxyStore

logger = logging.getLogger(__name__)


async def update_cf():
    """Crea la base de datos y las tablas necesarias."""
    proxy = "45.191.47.2:999"
    # 91.201.72.226:8090 44.215.73.168:8118
    cf_bypass = CloudflareBypass(
        target_url="https://solscan.io/account/", proxy=proxy, headless=False
    )
    await cf_bypass.run(update_cf=True)

    if cf_bypass.cf_clearance is None:
        logger.error("Failed to obtain CF clearance.")
        return

    logger.info(f"CF_CLEARANCE: {cf_bypass.cf_clearance.value}")

    store = ProxyStore()
    proxies = store.load()
    for p in proxies:
        if p.host == proxy:
            p.cf_clearance = cf_bypass.cf_clearance.value
    store._proxies = proxies
    store.save()
    logger.info("Proxy store updated with new CF clearance.")
    # solscan_client = SolscanClient(
    #     proxy=proxy, cf_clearance=cf_bypass.cf_clearance.value
    # )


def cli():
    asyncio.run(update_cf())
