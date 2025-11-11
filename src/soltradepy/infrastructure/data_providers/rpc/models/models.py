from soltradepy.infrastructure.data_providers.base_model import APIBaseModel


class RPCTokenAccounts(APIBaseModel):
    address: str
    mint: str
    owner: str
    amount: int
    delegated_amount: int
    frozen: bool


class RPCGetTokenAccountsResult(APIBaseModel):
    total: int
    limit: int
    cursor: str | None = None
    token_accounts: list[RPCTokenAccounts]


class RPCGetTokenAccountsResponse(APIBaseModel):
    jsonrpc: str
    result: RPCGetTokenAccountsResult
    id: int
    error: dict | None = None
