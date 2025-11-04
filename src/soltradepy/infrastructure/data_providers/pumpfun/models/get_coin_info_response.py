from typing import Optional
from pydantic import model_serializer
from soltradepy.infrastructure.data_providers.base_model import APIBaseModel


class CoinInfoResponse(APIBaseModel):
    mint: str
    name: str
    symbol: str
    description: str
    image_uri: str
    metadata_uri: str
    twitter: Optional[str]
    telegram: Optional[str]
    bonding_curve: str
    associated_bonding_curve: str
    creator: str
    created_timestamp: int
    raydium_pool: Optional[str]
    complete: bool
    virtual_sol_reserves: int
    virtual_token_reserves: int
    hidden: Optional[bool]
    total_supply: int
    website: Optional[str]
    show_name: bool
    last_trade_timestamp: int
    king_of_the_hill_timestamp: Optional[int]
    market_cap: float
    nsfw: bool
    market_id: Optional[str]
    inverted: Optional[bool]
    real_sol_reserves: int
    real_token_reserves: int
    livestream_ban_expiry: int
    last_reply: int
    reply_count: int
    is_banned: bool
    is_currently_live: bool
    initialized: bool
    video_uri: Optional[str]
    updated_at: Optional[int]
    pump_swap_pool: Optional[str]
    ath_market_cap: float
    ath_market_cap_timestamp: int
    banner_uri: Optional[str]
    hide_banner: bool
    livestream_downrank_score: int | None = None
    usd_market_cap: float

    @model_serializer
    def serializar(self):
        return {
            "mint": self.mint,
            "name": self.name,
            "symbol": self.symbol,
            "description": self.description,
            "metadata_uri": self.metadata_uri,
            "twitter": self.twitter,
            "telegram": self.telegram,
            "creator": self.creator,
            "created_timestamp": self.created_timestamp,
            "website": self.website,
            "pump_swap_pool": self.pump_swap_pool,
            "ath_market_cap": self.ath_market_cap,
            "ath_market_cap_timestamp": self.ath_market_cap_timestamp,
        }
