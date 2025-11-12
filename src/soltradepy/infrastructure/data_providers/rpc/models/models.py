from pydantic import Field, model_validator

from soltradepy.infrastructure.data_providers.base_model import APIBaseModel


class RPCResponse(APIBaseModel):
    jsonrpc: str
    result: dict
    id: int
    error: dict | None = None


# -----------------------------------GetTokenAccounts Models-----------------------------------#
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


# -----------------------------------GetTransaction Models-----------------------------------#
class RPCMetaTransaction(APIBaseModel):
    post_balances: list = Field(..., alias="postBalances")
    pre_balances: list = Field(..., alias="preBalances")
    delta_balances: list = []

    # Calulate deltabalance and added as new atribute
    @model_validator(mode="after")
    def calculate_delta_balance(self):
        pre_balances = self.pre_balances
        post_balances = self.post_balances
        self.delta_balances = [
            post - pre for post, pre in zip(post_balances, pre_balances)
        ]
        return self


class RPCMessageModel(APIBaseModel):
    account_keys: list = Field(..., alias="accountKeys")


class RPCTransaction(APIBaseModel):
    message: RPCMessageModel


class RPCGetTransactionResult(APIBaseModel):
    meta: RPCMetaTransaction
    transaction: RPCTransaction
    to_pk: str | None = None
    from_pk: str | None = None
    sol_amount: float | None = None
    send_sol_amount: float | None = None

    @model_validator(mode="after")
    def set_to_pk(self):
        if self.to_pk is not None:
            try:
                index = self.transaction.message.account_keys.index(self.to_pk)
                self.sol_amount = abs(
                    self.meta.pre_balances[index] - self.meta.post_balances[index]
                )
            except Exception:
                self.sol_amount = None
        return self

    @model_validator(mode="after")
    def set_from_pk(self):
        if self.from_pk is not None:
            try:
                index = self.transaction.message.account_keys.index(self.from_pk)
                self.send_sol_amount = abs(
                    self.meta.pre_balances[index] - self.meta.post_balances[index]
                )
            except Exception:
                self.send_sol_amount = None
        return self
