from sqlmodel import Session

from soltradepy.domain.core.models.wallet_entity import UserWallet
from soltradepy.domain.pumpfun.models.coin_info_entity import CoinInfo
from soltradepy.infrastructure.data_providers.pumpfun.pumpfun_client import (
    PumpfunClient,
)
from soltradepy.services.pumpfun.coin_info_service import CoinInfoService
from soltradepy.storage.pumpfun.coin_info_store import CoinInfoRepository
from soltradepy.storage.pumpfun.user_created_coins_store import (
    UserWalletRepository,
)


class PumpfunService:
    """Service for interacting with the Pumpfun data provider."""

    def __init__(self, session: Session, client: PumpfunClient | None = None):
        proxy = "144.31.26.218:3128"
        # proxy = "4.149.153.123:312"
        self.client = client or PumpfunClient(proxy=proxy)
        self.coin_info_service = CoinInfoService(self.client, session)
        self.coin_info_repo = CoinInfoRepository(session)
        self.user_wallet_repo = UserWalletRepository(session)

    async def sync_coin_info(self, token_address: str) -> CoinInfo | None:
        """Synchronize coin information with the SQL database."""
        response = await self.client.get_coin_info(token_address=token_address)
        token = CoinInfo.model_validate(response)
        coin = self.coin_info_repo.save(token)

        return coin

    async def sync_user_created_coins_for_user_wallet(
        self, wallet_address: str
    ) -> UserWallet | None:
        response = await self.client.get_user_created_coins(user_id=wallet_address)
        response = {
            "public_key": wallet_address,
            "created_tokens_count": response.count,
        }
        # wallet = UserWallet.model_validate(response)
        wallet = self.user_wallet_repo.save(fields=response)

        return wallet
