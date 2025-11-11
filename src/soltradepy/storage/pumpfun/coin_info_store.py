import logging

from sqlmodel import select

from soltradepy.domain.pumpfun.models.coin_info_entity import CoinInfo
from soltradepy.infrastructure.repository.base_repository import BaseRepository

logger = logging.getLogger(__name__)


class CoinInfoRepository(BaseRepository[CoinInfo]):
    def save(self, token: CoinInfo) -> CoinInfo | None:
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
            return token

        except Exception as e:
            self.session.rollback()
            logger.exception(f"Error saving coin info for mint {token.mint}: {e}")
            raise

    def update(self, data: dict) -> CoinInfo | None:
        """
        Store para actualizar información de monedas.
        Args:
            data: Información de la moneda a actualizar
        """
        try:
            stmt = select(CoinInfo).where(CoinInfo.mint == data["mint"])
            existing = self.session.scalar(stmt)
            coin = None

            if existing:
                logger.info(f"Updating coin info for mint {data['mint']}")
                for key, value in data.items():
                    if key != "id":
                        setattr(existing, key, value)
                coin = existing
            else:
                logger.warning(f"{data['mint']} was not found.")

            self.session.commit()
            return coin

        except Exception as e:
            self.session.rollback()
            logger.exception(f"Error saving coin info for mint {data['mint']}: {e}")
            raise
