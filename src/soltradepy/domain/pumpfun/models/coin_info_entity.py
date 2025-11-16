from sqlmodel import Field, SQLModel


class CoinInfo(SQLModel, table=True):
    """
    Tabla para almacenar información básica de monedas.
    """

    __tablename__ = "coin_info"  # type: ignore

    mint: str = Field(primary_key=True)  # dirección del token
    name: str | None = None
    symbol: str | None = None
    description: str | None = None
    image_uri: str | None = None
    metadata_uri: str | None = None
    twitter: str | None = None
    telegram: str | None = None
    bonding_curve: str | None = None
    associated_bonding_curve: str | None = None
    creator: str | None = None
    created_timestamp: int | None = None
    raydium_pool: str | None = None
    complete: bool | None = None
    website: str | None = None
    market_cap: float | None = None
    pump_swap_pool: str | None = None
    ath_market_cap: float | None = None
    ath_market_cap_timestamp: int | None = None
    usd_market_cap: float | None = None
    uri_size: int | None = None
    uri_json: str | None = None
    mayhem_state: int | None = None  # 1= active, 2 = completed
