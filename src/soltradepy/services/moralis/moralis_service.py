from sqlmodel import Session

from soltradepy.infrastructure.data_providers.moralis.moralis_client import (
    MoralisClient,
)
from soltradepy.services.moralis.graduated_tokens_service import (
    GraduatedTokensSyncSQLService,
)


class MoralisService:
    """Facade service for Moralis-related operations."""

    def __init__(self, api_key: str, session: Session):
        self.client = MoralisClient(api_key)
        self.graduated_tokens_sql_service = GraduatedTokensSyncSQLService(
            self.client, session
        )

    # ejemplo de fachada
    async def sync_graduated_tokens(self, limit: int = 10):
        """Facade method to sync graduated tokens."""
        return await self.graduated_tokens_sql_service.sync_next_page(limit=limit)
