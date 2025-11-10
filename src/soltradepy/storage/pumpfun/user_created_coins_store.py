import logging

from sqlmodel import select

from soltradepy.domain.core.models.wallet_entity import UserWallet
from soltradepy.infrastructure.repository.base_repository import BaseRepository

logger = logging.getLogger(__name__)


class UserWalletRepository(BaseRepository[UserWallet]):
    def save(self, fields: dict) -> UserWallet | None:
        """
        Store para persistir información de user wallet coins created.
        Args:
            wallet: Wallet's Public Key
        """
        try:
            stmt = select(UserWallet).where(
                UserWallet.public_key == fields["public_key"]
            )
            existing = self.session.scalar(stmt)

            if existing:
                wallet = existing
                logger.info(f"Updating user wallet for address {fields['public_key']}")
                for key, value in fields.items():
                    if key != "id":
                        setattr(existing, key, value)
            else:
                wallet = UserWallet.model_validate(fields)
                logger.info(
                    f"Inserting new user wallet for address {wallet.public_key}"
                )
                self.session.add(wallet)

            self.session.commit()
            return wallet

        except Exception as e:
            self.session.rollback()
            logger.exception(
                f"Error saving user wallet for address {fields['public_key']}: {e}"
            )
            raise
