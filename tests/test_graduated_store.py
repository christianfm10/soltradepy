from soltradepy.domain.moralis.models.graduated_token_entity import GraduatedToken


# from soltradepy.infrastructure.database import get_session
import soltradepy.storage.graduated_tokens_store as store_module
from soltradepy.storage.graduated_tokens_store import (
    GraduatedTokensSQLStore,
)
from sqlmodel import Session
from sqlalchemy import text


# def test_save_tokens_inserts_data(store):
#     token = GraduatedToken(
#         token_address="0x123",
#         name="TestToken",
#         symbol="TT",
#         logo=None,
#         decimals=6,
#         price_native="0.000001",
#         price_usd="0.01",
#         liquidity=1000.0,
#         fully_diluted_valuation=100000.0,
#         graduated_at="2025-01-01T00:00:00.000Z",
#     )

#     store.save_tokens([token])

#     tokens = store.session.exec(
#         "SELECT token_address, name FROM graduated_tokens"
#     ).all()

#     assert len(tokens) == 1
#     assert tokens[0][0] == "0x123"


def test_save_tokens_inserts_data(in_memory_db):

    from datetime import datetime

    store = GraduatedTokensSQLStore()

    token = GraduatedToken(
        token_address="0x123",
        name="TestToken",
        symbol="TT",
        logo=None,
        decimals=6,
        price_native="0.000001",
        price_usd="0.01",
        liquidity=1000.0,
        fully_diluted_valuation=100000.0,
        graduated_at=datetime.fromisoformat(
            "2025-01-01T00:00:00.000Z".replace("Z", "+00:00")
        ),
    )

    store.save_sql([token])

    # Recuperar manualmente para verificar
    with store_module.get_session() as session:
        result = session.exec(
            text("SELECT token_address, name FROM graduated_tokens")
        ).all()
    assert len(result) == 1
    assert result[0][0] == "0x123"
