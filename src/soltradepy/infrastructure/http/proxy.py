from concurrent.futures import (
    ALL_COMPLETED,
    ThreadPoolExecutor,
    wait,
)

import httpx
from bs4 import BeautifulSoup

NUM_THREADS = 20


def random_proxies(
    country: str | None = None, google_verified: bool = False
) -> list[str] | None:
    """Returns a 'random' proxy (ip:port) from the currently configured list.

    This is accomplished by testing each proxy concurrently until we find one that works.
    """

    validate_proxy_timeout = 2 if country or google_verified else 1

    proxy_list = get_proxies(country, google_verified)

    thread_list = []
    pool = ThreadPoolExecutor(NUM_THREADS)

    for proxy in proxy_list:
        proxy_thread = pool.submit(
            validate_proxy,
            proxy=proxy,
            timeout=validate_proxy_timeout,
        )
        thread_list.append(proxy_thread)

    wait(thread_list, return_when=ALL_COMPLETED)
    valid_proxy_list = [proxy.result() for proxy in thread_list if proxy.result()]

    if valid_proxy_list:
        return valid_proxy_list
    else:
        raise Exception(
            "No working proxies were found at this time, please try again later."
        )


def list_proxies(
    country: str | None = None, google_verified: bool = False
) -> list[str]:
    """Lists all proxies from the currently configured list."""
    proxy_list = get_proxies(country, google_verified)

    return proxy_list


def get_proxies(country: str | None = None, google_verified: bool = False) -> list[str]:
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

        proxy = f"{ip_address}:{port}"

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


def validate_proxy(proxy: str, timeout: float) -> str | None:
    """
    Valida si un proxy está funcionando correctamente usando httpx.
    Devuelve el proxy si es válido, o None si falla.
    """
    url = "https://www.google.com"
    url = "https://api-v2.solscan.io/v2/account/funded_by?address=3PFkJVowwwxqhk3Z4PonV5ibsimFvXRQWiU3mAzwoaKv"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0",
    }
    proxy_obj = httpx.Proxy(f"http://{proxy}")

    try:
        with httpx.stream(
            "GET", url, headers=headers, proxy=proxy_obj, timeout=timeout
        ) as response:
            # Si el código de estado es 200, el proxy respondió correctamente
            if response.status_code == 200 or response.status_code == 403:
                return proxy
    except Exception:
        # Si ocurre cualquier error, el proxy no es válido
        return None

    return None
