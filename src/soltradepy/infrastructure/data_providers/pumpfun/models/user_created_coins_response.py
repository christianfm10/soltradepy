from soltradepy.infrastructure.data_providers.base_model import APIBaseModel


class UserCreatedCoin(APIBaseModel):
    name: str
    symbol: str
    mint: str
    bonding_curve: str


class UserCreatedCoinsResponse(APIBaseModel):
    coins: list[UserCreatedCoin]
    count: int
