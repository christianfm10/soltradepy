from concurrent.futures import (
    ALL_COMPLETED,
    ThreadPoolExecutor,
    wait,
)
from enum import Enum

import httpx
from bs4 import BeautifulSoup

from soltradepy.infrastructure.http.models import Proxy

NUM_THREADS = 20


class Host(Enum):
    GOOGLE = "GOOGLE"
    SOLSCAN = "SOLSCAN"
    IPIFY = "IPIFY"


CONFIGS = {
    Host.GOOGLE: {
        "url": "https://www.google.com",
        "headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0",
        },
        "params": {},
    },
    Host.IPIFY: {
        "url": "https://api.ipify.org/?format=json",
        "headers": {
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0",
        },
        "params": {},
    },
    Host.SOLSCAN: {
        "url": "https://api-v2.solscan.io/v2/account/funded_by",
        "headers": {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate",
            "Origin": "https://solscan.io",
            "Referer": "https://solscan.io",
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:136.0) Gecko/20100101 Firefox/136.0",
        },
        "params": {"address": "3PFkJVowwwxqhk3Z4PonV5ibsimFvXRQWiU3mAzwoaKv"},
    },
}


class NoValidProxiesException(Exception):
    """Exception raised when no valid proxies are found."""

    pass


def random_proxies(
    country: str | None = None, google_verified: bool = False, host=Host.GOOGLE
) -> list[Proxy]:
    """Returns a 'random' proxy (ip:port) from the currently configured list.

    This is accomplished by testing each proxy concurrently until we find one that works.
    """

    validate_proxy_timeout = 2 if country or google_verified else 1

    proxy_list = get_proxies(country, google_verified)

    valid_proxy_list = validate_proxies(
        proxy_list=proxy_list, timeout=validate_proxy_timeout, host=host
    )
    # valid_proxy_list = [proxy.result() for proxy in thread_list if proxy.result()]

    if valid_proxy_list:
        # proxy_list = [Proxy(host=p, alive=True) for p in valid_proxy_list]
        return valid_proxy_list
    else:
        raise NoValidProxiesException(
            "No working proxies were found at this time, please try again later."
        )


def list_proxies(
    country: str | None = None, google_verified: bool = False
) -> list[Proxy]:
    """Lists all proxies from the currently configured list."""
    proxy_list = get_proxies(country, google_verified)

    return proxy_list


def get_proxies(
    country: str | None = None, google_verified: bool = False
) -> list[Proxy]:
    """Gets a list of proxies from https://www.sslproxies.org by scraping the proxy table."""
    proxy_list = []

    website = httpx.get(
        url="https://free-proxy-list.net/en/ssl-proxy.html",
        timeout=3,
    )

    soup = BeautifulSoup(website.text, "html.parser")
    tbody = None
    if soup:
        table = soup.find("table")
        if table:
            tbody = table.find("tbody")

    if tbody is None:
        raise Exception("Could not find proxy table content!")

    for table_entry in tbody.find_all("tr"):  # type:ignore
        entry_elements = [td.text.strip() for td in table_entry.find_all("td")]
        ip_address = entry_elements[0]
        port = entry_elements[1]
        country_code = entry_elements[2]  # Two digit ISO country code
        is_google_verified = True if entry_elements[5] == "yes" else False

        # proxy = f"{ip_address}:{port}"
        proxy = Proxy(host=f"{ip_address}:{port}")

        # If the user specified filters, respect them here
        if (
            (country is not None and country_code == country)
            and (google_verified and is_google_verified)
        ):  # pragma: no cover - cannot reliably get country + google-verified filtered results
            proxy_list.append(proxy)
        elif (country is not None and country_code == country) and (
            not google_verified
        ):
            proxy_list.append(proxy)
        elif (country is None) and (google_verified and is_google_verified):
            proxy_list.append(proxy)
        elif (country is None) and (google_verified is False):
            proxy_list.append(proxy)

    if len(proxy_list) == 0:
        raise ValueError(
            "There are no proxies with your specified criteria at this time. Please try again later."
        )

    return proxy_list


def validate_proxies(
    proxy_list: list[Proxy], timeout: float, host: Host = Host.GOOGLE
) -> list[Proxy]:
    thread_list = []
    pool = ThreadPoolExecutor(NUM_THREADS)

    for proxy in proxy_list:
        proxy_thread = pool.submit(
            validate_proxy,
            proxy=proxy,
            timeout=timeout,
            host=host,
        )
        thread_list.append(proxy_thread)

    wait(thread_list, return_when=ALL_COMPLETED)
    valid_proxy_list = [proxy.result() for proxy in thread_list if proxy.result()]
    alive_proxies = [p for p in valid_proxy_list if p.alive]

    return alive_proxies
    return valid_proxy_list


def validate_proxy(
    proxy: Proxy, timeout: float, host: Host = Host.GOOGLE
) -> Proxy | None:
    """
    Valida si un proxy está funcionando correctamente usando httpx.
    Devuelve el proxy si es válido, o None si falla.
    """
    url = CONFIGS[host].get("url", "https://google.com")
    headers = CONFIGS[host].get("headers", {})
    params = CONFIGS[host].get("params", {})
    proxy_obj = httpx.Proxy(f"http://{proxy.host}")

    try:
        with httpx.stream(
            "GET", url, headers=headers, proxy=proxy_obj, params=params, timeout=timeout
        ) as response:
            # Si el código de estado es 200, el proxy respondió correctamente
            if response.status_code == 200:
                proxy.alive = True
                return proxy
    except Exception:
        # Si ocurre cualquier error, el proxy no es válido
        proxy.alive = False
        return proxy

    proxy.alive = False
    return proxy
