import asyncio

import pytest

from soltradepy.infrastructure.data_providers.solscan.solscan_client import (
    SolscanClient,
)
from soltradepy.infrastructure.data_providers.utils import create_clients
from soltradepy.infrastructure.http.models import Proxy
from soltradepy.infrastructure.http.proxy import Host, random_proxies, validate_proxies
from soltradepy.infrastructure.http.store import ProxyStore
from soltradepy.infrastructure.http.worker import create_queue, create_tasks


@pytest.fixture
def proxies():
    proxies = [
        "193.163.201.90:8080",
        "4.149.153.123:3128",
        "44.215.73.168:8118",
        "167.71.177.246:2525",
        "144.31.26.218:3128",
        "194.58.34.63:3128",
    ]
    return proxies


@pytest.fixture
def fake_proxies(proxies):
    fake_proxies = [Proxy(host=p, alive=False) for p in proxies]

    return fake_proxies


@pytest.mark.skip
def test_random_proxies():
    # result = random_proxies()

    store = ProxyStore()
    store.load()
    # store.add_proxies(result)
    store._proxies = validate_proxies(store._proxies, timeout=5, host=Host.IPIFY)

    # print(result)
    print(len(store.filter_alive()))
    store.save()


@pytest.mark.asyncio
async def test_client():
    # result = random_proxies()
    print("___________________________________________")
    max_retries = 1
    addresses = [
        "DALASbVfzSWnvQ2jmXanU5C3cWPBvM25xmmnBZar72pj",
        "DMo6DJs81fMdwE4cX2WWmDeKoDAbwCvoEZ8fXQfK8XCh",
        "EveCGJLF3tvJrq21g7Cr7pBjowKfgBxBJan99rAHa3kz",
        "2ptGcKCHtHRmajB9qV5R9tZb6nVwXXT6o9QZvzQ7mA3n",
        "vaMS6r75negw3AdVetNdySvz69tzR6uLvWyPNeng5A4",
        "iffPDmLdBb6byCymsNZsA7EK9heZECT8t4BtoyVG87L",
        "2ZXG2twdRqaKYCrGNcE4q6r7Zvcp4Gh3j2jXufgR8Mni",
        "4npiVLQhSoLiov1AYdppWVLt6f56ovUQTa7K6Jmu5b4M",
        "8Xt4mnCcz4HucZkGs4NkRa6eckzbSR6XWzuXSqeC7Hyr",
        "C8jFdNNDnB5r6iAqJznh3GyktpZsHzSdRVyxgBnc3uoe",
        "3SqdqYLDtmYcvRk31Ut5FbLqSZybKCxUVMxUXYKjLA73",
        "FWWJ8kiaCqsDNw3Q5TdEu43gTUHQtGddzRUj9YNr2kU5",
        "7tgxK5kpnKyhbihbofJKMJBmV5VfAgNGmSYyqJS1xe2v",
        "EeC1oXAh3Wn8TrY2Bjbtygf1QXRQtZrJCsUaCNEyHZdL",
        "K4htCPfif7xhYS8NM3BWsfJXMdPFwNy8ko1rHXkyvNu",
        "D61gjnhbtYnduoaHKJVYBNqKn38u9FVBwcYPpiwo8jrt",
    ]
    queue = create_queue(addresses)
    results = []
    store = ProxyStore()
    proxies = store.load()
    clients = create_clients(proxies=proxies, client_type=SolscanClient)
    if clients[1].proxy is not None:
        clients[1].proxy += "_bad"
    # clients[2].proxy += "_bad"
    tasks = create_tasks(proxies, clients, queue, results, max_retries)

    # tasks = await monitor_workers(tasks, queue)

    await queue.join()
    for t in tasks:
        if not t.done():
            t.cancel()

    await asyncio.gather(*tasks, return_exceptions=True)
    print("Results :", results)


def test_add_from_strings(proxies):
    store = ProxyStore()
    store.add_from_strings(proxies=proxies)

    assert len(proxies) == len(store._proxies)


def test_add_proxies(fake_proxies):
    store = ProxyStore()
    store.add_proxies(fake_proxies)

    assert len(fake_proxies) == len(store._proxies)


def test_filter_alive(fake_proxies):
    store = ProxyStore()
    store.add_proxies(fake_proxies)

    alives = store.filter_alive()
    assert len(alives) == 0


def test_save_and_load_proxies(proxies, tmp_path):
    store = ProxyStore()
    store.add_from_strings(proxies=proxies)

    file_path = tmp_path / "proxies.json"
    store.save(path=file_path)

    assert file_path.exists

    new_store = ProxyStore()
    new_store.load(path=file_path)

    assert len(store._proxies) == len(new_store._proxies)

    assert [p.model_dump() for p in store._proxies] == [
        p.model_dump() for p in new_store._proxies
    ]
