from sqlalchemy import text

from soltradepy.domain.moralis.models.graduated_token_entity import GraduatedToken
from soltradepy.storage.graduated_tokens_store import (
    GraduatedTokenRepository,
)


def test_save_tokens_inserts_data(session):
    """Test that save method inserts new graduated tokens into the database."""

    from datetime import datetime

    repository = GraduatedTokenRepository(session)

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

    repository.save([token])

    # Recuperar manualmente para verificar
    result = session.exec(
        text("SELECT token_address, name FROM graduated_tokens")
    ).all()

    assert len(result) == 1
    assert result[0][0] == "0x123"
