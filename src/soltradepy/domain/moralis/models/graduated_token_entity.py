import datetime

from sqlmodel import Field, SQLModel


class GraduatedToken(SQLModel, table=True):
    """
    Tabla simple para almacenar los tokens graduados desde Moralis.
    Ideal para backtesting / histórico.
    """

    __tablename__ = "graduated_tokens"  # type: ignore

    token_address: str = Field(primary_key=True)  # único garantizado
    name: str | None = None
    symbol: str | None = None
    logo: str | None = None

    decimals: int
    price_native: float
    price_usd: float
    liquidity: float
    fully_diluted_valuation: float

    graduated_at: (
        datetime.datetime
    )  # convertir string ISO → datetime en el sync service
    stored_at: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now(datetime.UTC)
    )  # tracking interno
