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
    def save(self, new_tokens: list[GraduatedToken]) -> bool:
        """
        Store para persistir graduated tokens.
        Args:
            new_tokens: lista de graduated tokens a guardar
        """
        token = None
        try:
            for token in new_tokens:
                stmt = select(GraduatedToken).where(
                    GraduatedToken.token_address == token.token_address
                )
                existing = self.session.scalar(stmt)

                if existing:
                    logger.info(
                        f"[bold green]Updating coin info for mint {token.token_address}[/bold green]"
                    )
                    for key, value in token.model_dump().items():
                        if key != "id":
                            setattr(existing, key, value)
                else:
                    logger.info(
                        f"[bright_green]Inserting new coin info for mint {token.token_address}[/bright_green]"
                    )
                    self.session.add(token)

                self.session.commit()
            return True

        except Exception as e:
            self.session.rollback()
            if token is not None:
                logger.exception(
                    f"Error saving coin info for mint {token.token_address}: {e}"
                )
            raise
