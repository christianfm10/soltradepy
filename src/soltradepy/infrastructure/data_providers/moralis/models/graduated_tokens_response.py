# soltradepy/infrastructure/data_providers/moralis/models/graduated_tokens_response.py

from datetime import datetime

from pydantic import Field, field_validator

from soltradepy.infrastructure.data_providers.base_model import APIBaseModel


class MoralisGraduatedToken(APIBaseModel):
    token_address: str = Field(..., alias="tokenAddress")
    name: str
    symbol: str
    logo: str | None
    decimals: int
    price_native: float = Field(..., alias="priceNative")
    price_usd: float = Field(..., alias="priceUsd")
    liquidity: float
    fully_diluted_valuation: float = Field(default=0.0, alias="fullyDilutedValuation")
    graduated_at: datetime = Field(..., alias="graduatedAt")

    model_config = {
        "populate_by_name": True,
        "from_attributes": True,
    }

    @field_validator("fully_diluted_valuation", mode="before")
    def none_to_zero(cls, v):
        if v is None:
            return 0.0
        return v


class MoralisGraduatedTokensResponse(APIBaseModel):
    result: list[MoralisGraduatedToken]
    page_size: int = Field(..., alias="pageSize")
    page: int
    cursor: str | None
