# storage/graduated_tokens_store.py
import json
from pathlib import Path

from soltradepy.infrastructure.database import get_session

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
    def save_sql(new_tokens: list) -> None:
        """
        Store para persistir tokens graduados en SQLite.
        Hace UPSERT (merge) — si el token_address ya existe, lo actualiza.
        """
        with get_session() as session:
            for token in new_tokens:
                print(type(token))
                session.merge(token)  # UPSERT automático
            session.commit()
