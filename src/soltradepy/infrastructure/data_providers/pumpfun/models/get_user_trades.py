from pydantic import Field, model_validator

from soltradepy.infrastructure.data_providers.base_model import APIBaseModel


class Trades(APIBaseModel):
    slot_index_id: str = Field(..., alias="slotIndexId")
    tx: str
    timestamp: str
    user_address: str = Field(..., alias="userAddress")
    type: str
    is_bonding_curve: bool = Field(..., alias="isBondingCurve")


class UserTradesResponse(APIBaseModel):
    """User Trades on token Response Model"""

    user_trades: list[Trades]

    @model_validator(mode="before")
    def set_user_trades(cls, data):
        if not isinstance(data, dict):
            raise ValueError("Expected a dictionary")

        if len(data) != 1:
            raise ValueError("Expected only one user address in the response")

        try:
            (_, trades) = next(iter(data.items()))
        except StopIteration:
            raise ValueError("Response data is empty")

        return {"user_trades": trades}
