# soltradepy/infrastructure/data_providers/moralis/models/graduated_tokens_response.py

from soltradepy.infrastructure.data_providers.base_model import APIBaseModel
from pydantic import Field
from datetime import datetime
from typing import Optional, List


class MoralisGraduatedToken(APIBaseModel):
    token_address: str = Field(..., alias="tokenAddress")
    name: str
    symbol: str
    logo: Optional[str]
    decimals: int
    price_native: float = Field(..., alias="priceNative")
    price_usd: float = Field(..., alias="priceUsd")
    liquidity: float
    fully_diluted_valuation: float = Field(..., alias="fullyDilutedValuation")
    graduated_at: datetime = Field(..., alias="graduatedAt")

    model_config = {
        "populate_by_name": True,
        "from_attributes": True,
    }


class MoralisGraduatedTokensResponse(APIBaseModel):
    result: List[MoralisGraduatedToken]
    page_size: int = Field(..., alias="pageSize")
    page: int
    cursor: Optional[str]
