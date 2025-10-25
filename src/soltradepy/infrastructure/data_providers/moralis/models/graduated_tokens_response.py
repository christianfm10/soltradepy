# soltradepy/infrastructure/data_providers/moralis/models/graduated_tokens_response.py

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
import json

class GraduatedToken(BaseModel):
    """
    Representa un token individual en la respuesta de Moralis.
    """
    # TODO: definir campos exactos según la response oficial


class GraduatedTokensResponse(BaseModel):
    """
    Representa la respuesta completa del endpoint
    'get_graduated_tokens_by_exchange' de Moralis.
    """
    # TODO: definir campos exactos según la response oficial
    # ejemplo probable: items: list[GraduatedToken]
    pass

# def pydantic_repr(cls):
    # def __str__(self):
    #     return json.dumps(self.model_dump(), indent=2, ensure_ascii=False)

    # cls.__str__ = __str__
    # cls.__repr__ = __str__
    # return cls

class APIBaseModel(BaseModel):
    def __str__(self):
        return json.dumps(self.model_dump(), indent=2, ensure_ascii=False)

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
    graduated_at: str = Field(..., alias="graduatedAt")

    model_config = {
        "populate_by_name": True,
        "from_attributes": True
    }

class MoralisGraduatedTokensResponse(APIBaseModel):
    result: List[MoralisGraduatedToken]
    page_size: int = Field(..., alias="pageSize")
    page: int
    cursor: Optional[str]