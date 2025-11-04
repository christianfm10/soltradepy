import logging

from sqlmodel import select

from soltradepy.domain.pumpfun.models.coin_info_entity import CoinInfo
from soltradepy.infrastructure.repository.base_repository import BaseRepository

logger = logging.getLogger(__name__)


class CoinInfoRepository(BaseRepository[CoinInfo]):
    def save(self, token: CoinInfo) -> bool:
        """
        Store para persistir información de monedas.
        Args:
            token: Información de la moneda a guardar
        """
        try:
            stmt = select(CoinInfo).where(CoinInfo.mint == token.mint)
            existing = self.session.scalar(stmt)

            if existing:
                logger.info(f"Updating coin info for mint {token.mint}")
                for key, value in token.model_dump().items():
                    if key != "id":
                        setattr(existing, key, value)
            else:
                logger.info(f"Inserting new coin info for mint {token.mint}")
                self.session.add(token)

            self.session.commit()

            return True

        except Exception as e:
            self.session.rollback()
            logger.exception(f"Error saving coin info for mint {token.mint}: {e}")
            raise
