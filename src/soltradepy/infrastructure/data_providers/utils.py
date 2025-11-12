from soltradepy.infrastructure.data_providers.base_client import BaseClient
from soltradepy.infrastructure.http.models import Proxy


def create_clients(proxies: list[Proxy], client_type: type[BaseClient]):
    clients = [
        client_type(proxy=p.host, cf_clearance=p.cf_clearance, timeout=20)
        for p in proxies
    ]
    return clients


def lamports_to_sol(lamports: int) -> float:
    """
    Convierte lamports a SOL.

    Args:
        lamports (int): Cantidad de lamports.

    Returns:
        float: Cantidad equivalente en SOL.
    """
    value_sol = lamports / 1_000_000_000
    return value_sol
