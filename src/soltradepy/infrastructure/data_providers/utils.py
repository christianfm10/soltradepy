from soltradepy.infrastructure.data_providers.base_client import BaseClient
from soltradepy.infrastructure.http.models import Proxy


def create_clients(proxies: list[Proxy], client_type: type[BaseClient]):
    clients = [
        client_type(proxy=p.host, cf_clearance=p.cf_clearance, timeout=20)
        for p in proxies
    ]
    return clients
