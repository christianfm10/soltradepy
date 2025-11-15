import asyncio
import logging

from sqlmodel import text

from soltradepy.infrastructure.async_utils.worker import monitor_workers
from soltradepy.infrastructure.config.env import get_settings
from soltradepy.infrastructure.data_providers.solscan.models.transfer import (
    TransferResponse,
)
from soltradepy.infrastructure.data_providers.solscan.solscan_client import (
    SolscanClient,
)
from soltradepy.infrastructure.data_providers.utils import create_clients
from soltradepy.infrastructure.database import get_session
from soltradepy.infrastructure.http.store import ProxyStore
from soltradepy.infrastructure.http.worker import create_queue, create_tasks

logging.getLogger("httpx").setLevel(logging.WARNING)
settings = get_settings()


USDC = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"


async def main():
    """Update UserWalletModel's info, checking if has interaction with 21w wallet."""
    session = get_session()
    logging.info("Select UserWalletModels without is_isma info...")
    # stmt = "SELECT public_key as address FROM user_wallets WHERE funded_wallet IS NULL"
    stmt = """
    SELECT public_key as address
    FROM user_wallets 
        LEFT JOIN coin_info as ci ON public_key = ci.creator
    WHERE has_21w_txns IS NULL
    ORDER BY created_timestamp DESC
    LIMIT 10;
    """
    wallets = session.execute(text(stmt)).mappings().all()
    # return
    params = [dict(w) for w in wallets]
    for p in params:
        p["to"] = "21wG4F3ZR8gwGC47CkpD6ySBUgH9AABtYMBWFiYdTTgv"
        p["token"] = USDC

    proxies = ProxyStore().load()

    clients = create_clients(proxies=proxies, client_type=SolscanClient)
    client_funcs = [c.get_transfers for c in clients]
    # for w in wallets:

    queue = create_queue(params)
    results: list[tuple[dict, str, TransferResponse]] = []
    max_retries = 1
    logging.info("Fetching funding info from Solscan...")
    tasks = create_tasks(proxies, client_funcs, queue, results, max_retries)

    tasks = await monitor_workers(tasks, queue)

    await queue.join()
    for t in tasks:
        if not t.done():
            t.cancel()

    await asyncio.gather(*tasks, return_exceptions=True)
    print("Results length:", len(results))

    # repo = UserWalletRepository(session)
    for result in results:
        params, _, response = result
        address = params["address"]
        transfers = response.data
        if response.success:
            mapped_data = {
                "public_key": address,
                "has_21w_txns": True if len(transfers) > 0 else False,
            }
            # user = UserWallet.from_funded_by(funded_by.model_dump())
            # repo.save(fields=mapped_data)
            try:
                update_query = """
                    UPDATE user_wallets
                    SET has_21w_txns = :has_21w_txns
                    WHERE public_key = :public_key
                """
                session.execute(
                    text(update_query),
                    {
                        "has_21w_txns": mapped_data["has_21w_txns"],
                        "public_key": mapped_data["public_key"],
                    },
                )
                session.commit()
            except Exception as e:
                logging.error(f"Error updating wallet {address}: {e}")

    for c in clients:
        await c.close()


def cli():
    import asyncio

    asyncio.run(main())


if __name__ == "__main__":
    cli()
