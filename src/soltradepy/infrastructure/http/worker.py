import asyncio

from soltradepy.infrastructure.async_utils.worker import worker
from soltradepy.infrastructure.http.models import Proxy


def create_queue(addresses):
    queue = asyncio.Queue()
    for a in addresses:
        queue.put_nowait((a, 0))
    return queue


def create_tasks(proxies: list[Proxy], clients, queue, results, max_retries):
    tasks = [
        asyncio.create_task(
            worker(
                p.host, client.get_funded_by, queue, results, max_retries=max_retries
            )
        )
        for p, client in zip(proxies, clients)
    ]
    return tasks
