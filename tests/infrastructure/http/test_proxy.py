import pytest

from soltradepy.infrastructure.http.proxy import random_proxies


def test_proxy():
    result = random_proxies()
    print(result)
