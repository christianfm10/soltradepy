# storage/graduated_tokens_store.py
import json
import logging

from pathlib import Path

from sqlmodel import select

from soltradepy.infrastructure.database import get_session
from soltradepy.domain.moralis.models.graduated_token_entity import GraduatedToken

# from typing import TYPE_CHECKING

# if TYPE_CHECKING:

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


class GraduatedTokensSQLStore:

    @staticmethod
    def save_sql(new_tokens: list[GraduatedToken]) -> None:
        """
        Store para persistir tokens graduados en SQLite.
        Hace UPSERT (merge) — si el token_address ya existe, lo actualiza.
        """
        logger = logging.getLogger("GraduatedTokensSQLStore")
        with get_session() as session:
            try:
                for token in new_tokens:
                    # Check if token already exists using token_address as primary key
                    stmt = select(GraduatedToken).where(
                        GraduatedToken.token_address == token.token_address
                    )
                    existing = session.scalar(stmt)

                    if existing:
                        logger.warning(
                            f"Token {token.token_address} already exists. Skipping insert."
                        )
                    else:
                        logger.info(f"inserting new token {token.token_address}.")
                        session.add(token)  # upsert automático
            except Exception as e:
                session.rollback()
                logger.exception(f"Error saving token {token.token_address}: {e}")
                raise
