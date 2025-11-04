# storage/graduated_tokens_store.py
import json
import logging

from pathlib import Path

from sqlmodel import select

from soltradepy.domain.moralis.models.graduated_token_entity import GraduatedToken
from soltradepy.infrastructure.repository.base_repository import BaseRepository


DATA_PATH = Path(__file__).parent / "tokens_graduated.json"


class GraduatedTokensJSONStore:
    @staticmethod
    def load() -> list:
        if DATA_PATH.exists():
            return json.loads(DATA_PATH.read_text())
        return []

    @staticmethod
    def save(tokens: list) -> None:
        DATA_PATH.write_text(json.dumps(tokens, indent=2))

    @staticmethod
    def append(new_tokens: list) -> None:
        data = GraduatedTokensJSONStore.load()
        data.extend(new_tokens)
        GraduatedTokensJSONStore.save(data)

    # add clear method
    @staticmethod
    def clear() -> None:
        if DATA_PATH.exists():
            DATA_PATH.unlink()


logger = logging.getLogger(__name__)


class GraduatedTokenRepository(BaseRepository[GraduatedToken]):
    def save(self, new_tokens: list[GraduatedToken]) -> GraduatedToken:
        """
        Store para persistir graduated tokens.
        Args:
            new_tokens: lista de graduated tokens a guardar
        """
        try:
            for token in new_tokens:
                stmt = select(GraduatedToken).where(
                    GraduatedToken.token_address == token.token_address
                )
                existing = self.session.scalar(stmt)

                if existing:
                    logger.info(f"Updating coin info for mint {token.token_address}")
                    for key, value in token.model_dump().items():
                        if key != "id":
                            setattr(existing, key, value)
                    result = existing
                else:
                    logger.info(
                        f"Inserting new coin info for mint {token.token_address}"
                    )
                    self.session.add(token)
                    result = token

                self.session.commit()
            return result

        except Exception as e:
            self.session.rollback()
            logger.exception(f"Error saving coin info for mint {token.mint}: {e}")
            raise
