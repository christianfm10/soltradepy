from sqlmodel import Session

from soltradepy.domain.pumpfun.models.coin_info_entity import CoinInfo
from soltradepy.infrastructure.data_providers.pumpfun.pumpfun_client import (
    PumpfunClient,
)
from soltradepy.services.pumpfun.coin_info_service import CoinInfoService
from soltradepy.storage.pumpfun.coin_info_store import CoinInfoRepository


class PumpfunService:
    """Service for interacting with the Pumpfun data provider."""

    def __init__(self, session: Session, client: PumpfunClient | None = None):
        self.client = client or PumpfunClient()
        self.coin_info_service = CoinInfoService(self.client, session)
        self.coin_info_repo = CoinInfoRepository(session)
        # self.graduated_tokens_sql_service = GraduatedTokensSyncSQLService(self.client)

    async def sync_coin_info(self, token_address: str) -> CoinInfo | None:
        """Synchronize coin information with the SQL database."""
        response = await self.client.get_coin_info(token_address=token_address)
        token = CoinInfo.model_validate(response)
        coin = self.coin_info_repo.save(token)

        return coin
