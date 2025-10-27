from soltradepy.domain.moralis.models.graduated_token_entity import GraduatedToken
from soltradepy.infrastructure.data_providers.moralis.moralis_client import (
    MoralisClient,
)
from soltradepy.storage.graduated_tokens_store import (
    GraduatedTokensJSONStore,
    GraduatedTokensSQLStore,
)
from soltradepy.storage.cursor_state_store import CursorStateStore


class GraduatedTokensSyncJSONService:
    """Service to sync graduated tokens from Moralis and store them in JSON."""

    def __init__(self, client: MoralisClient):
        self.client = client

    async def sync_next_page(self, limit: int = 10):
        """Sync the next page of graduated tokens from Moralis."""
        last_cursor = CursorStateStore.load()
        response = await self.client.get_graduated_tokens_by_exchange_pumpfun(
            limit=limit, cursor=last_cursor
        )

        GraduatedTokensJSONStore.append(
            response.model_dump(mode="json").get("result", [])
        )
        CursorStateStore.save(response.cursor)

        return {
            "saved": len(response.result),
            "next_cursor": response.cursor,
        }


class GraduatedTokensSyncSQLService:
    """Service to sync graduated tokens from Moralis and store them in SQL."""

    def __init__(self, client: MoralisClient):
        self.client = client

    async def sync_next_page(self, limit: int = 10):
        """Sync the next page of graduated tokens from Moralis."""
        last_cursor = CursorStateStore.load()
        response = await self.client.get_graduated_tokens_by_exchange_pumpfun(
            limit=limit, cursor=last_cursor
        )
        tokens = [GraduatedToken.model_validate(token) for token in response.result]
        # tokens = [GraduatedToken(**token.model_dump()) for token in response.result]
        GraduatedTokensSQLStore.save_sql(tokens)
        CursorStateStore.save(response.cursor)

        return {
            "saved": len(response.result),
            "next_cursor": response.cursor,
        }
