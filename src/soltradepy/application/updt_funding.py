import asyncio
import logging

# from sqlalchemy import select
from sqlmodel import text

from soltradepy.domain.core.models.wallet_entity import UserWallet
from soltradepy.infrastructure.config.env import get_settings
from soltradepy.infrastructure.data_providers.solscan.models.funded_by import (
    FundedByResponse,
)
from soltradepy.infrastructure.data_providers.solscan.solscan_client import (
    SolscanClient,
)
from soltradepy.infrastructure.data_providers.utils import create_clients
from soltradepy.infrastructure.database import get_session
from soltradepy.infrastructure.http.store import ProxyStore
from soltradepy.infrastructure.http.worker import create_queue, create_tasks
from soltradepy.storage.pumpfun.user_created_coins_store import UserWalletRepository

# logging with colors, orange for warnings, red for errors, green for info, blue for debug
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logging.getLogger("httpx").setLevel(logging.WARNING)
settings = get_settings()


async def main():
    """Update UserWalletModel's funding info with funding info from Solscan."""
    session = get_session()
    logging.info("Select UserWalletModels without funding info...")
    stmt = "SELECT public_key as address FROM user_wallets WHERE funded_wallet IS NULL"
    wallets = session.execute(text(stmt)).mappings().all()

    proxies = ProxyStore().load()

    clients = create_clients(proxies=proxies, client_type=SolscanClient)

    queue = create_queue(wallets)
    results: list[tuple[dict, str, FundedByResponse]] = []
    max_retries = 1
    logging.info("Fetching funding info from Solscan...")
    tasks = create_tasks(proxies, clients, queue, results, max_retries)

    # tasks = await monitor_workers(tasks, queue)

    await queue.join()
    for t in tasks:
        if not t.done():
            t.cancel()

    await asyncio.gather(*tasks, return_exceptions=True)

    repo = UserWalletRepository(session)
    for result in results:
        _, _, response = result
        funded_by = response.data
        if funded_by:
            user = UserWallet.from_funded_by(funded_by.model_dump())
            repo.save(user)


def cli():
    import asyncio

    asyncio.run(main())


if __name__ == "__main__":
    cli()
