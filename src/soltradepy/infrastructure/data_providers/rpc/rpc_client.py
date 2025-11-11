from soltradepy.infrastructure.data_providers.base_client import BaseClient
from soltradepy.infrastructure.data_providers.rpc.models.models import (
    RPCGetTokenAccountsResponse,
    RPCGetTokenAccountsResult,
)


class RPCException(Exception):
    pass


class RPC_Client(BaseClient):
    BASE_URL = "https://api.mainnet-beta.solana.com"

    def __init__(
        self,
        base_url: str = "https://api.mainnet-beta.solana.com",
    ):
        super().__init__(base_url=base_url)

    async def get_token_accounts(
        self,
        owner: str,
        mint: str | None = None,
        show_zero_balance: bool = False,
        limit: int = 10,
    ) -> RPCGetTokenAccountsResult:
        """
        Obtiene las cuentas de tokens asociadas a una wallet

        Args:
            owner_address: Dirección de la wallet (base58)
            show_zero_balance: Si se deben incluir cuentas con saldo cero

        Returns:
            Diccionario con la información de las cuentas de tokens

        Raises:
            ValueError: Si la dirección es inválida
            Exception: Para errores RPC
        """
        method = "getTokenAccounts"
        params = {
            "limit": limit,
            "owner": owner,
            "options": {
                "showZeroBalance": show_zero_balance,
            },
            **({"mint": mint} if mint else {}),
        }

        payload = {"jsonrpc": "2.0", "id": 1, "method": method, "params": params}

        result = await self._fetch("POST", payload=payload)
        result = RPCGetTokenAccountsResponse(**result)

        if result.error is not None:
            raise RPCException(f"Error RPC: {result.error['message']}")

        return result.result
