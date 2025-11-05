from sqlmodel import Session

from soltradepy.domain.pumpfun.models.coin_info_entity import CoinInfo
from soltradepy.infrastructure.data_providers.pumpfun.pumpfun_client import (
    PumpfunClient,
)
from soltradepy.storage.pumpfun.coin_info_store import CoinInfoRepository


class CoinInfoService:
    """Service for interacting with the CoinInfo data provider."""

    def __init__(self, client: PumpfunClient, session: Session):
        self.client = client
        self.repository = CoinInfoRepository(session)

    async def sync_coin_info(self, token_address: str) -> CoinInfo | None:
        """Fetch coin info by token address from Pumpfun."""
        response = await self.client.get_coin_info(token_address=token_address)

        token = CoinInfo.model_validate(response)

        return self.repository.save(token)
