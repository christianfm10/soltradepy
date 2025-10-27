from soltradepy.infrastructure.data_providers.moralis.moralis_client import (
    MoralisClient,
)
from soltradepy.services.moralis.graduated_tokens_service import (
    GraduatedTokensSyncSQLService,
)


class MoralisService:
    """Facade service for Moralis-related operations."""

    def __init__(self, api_key: str):
        self.client = MoralisClient(api_key)
        self.graduated_tokens = GraduatedTokensSyncSQLService(self.client)

    # ejemplo de fachada
    async def sync_graduated_tokens(self, limit: int = 10):
        """Facade method to sync graduated tokens."""
        return await self.graduated_tokens.sync_next_page(limit=limit)
