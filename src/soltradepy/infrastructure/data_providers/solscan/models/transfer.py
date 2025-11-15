from soltradepy.infrastructure.data_providers.base_model import APIBaseModel


class Transfer(APIBaseModel):
    activity_type: str
    amount: float
    block_id: int
    block_time: int
    flow: str
    from_address: str
    from_token_account: str
    to_address: str
    to_token_account: str
    token_address: str
    token_decimals: int
    trans_id: str
    value: float


class TransferResponse(APIBaseModel):
    data: list[Transfer]
    success: bool
