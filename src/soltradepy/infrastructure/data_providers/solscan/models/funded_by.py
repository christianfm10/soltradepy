import datetime
from pydantic import model_serializer, model_validator

from soltradepy.infrastructure.data_providers.base_model import APIBaseModel


# @dataclass
class AccountMetadata(APIBaseModel):
    account_address: str | None = None
    account_icon: str | None = None
    account_label: str | None = None
    account_tags: list[str] | None = None
    account_type: str | None = None


class MetadaBase(APIBaseModel):
    accounts: dict[str, AccountMetadata]
    tags: dict[str, dict]
    tokens: dict[str, dict]
    # success: bool
    nftCollections: dict[str, dict]
    nftMarketplaces: dict[str, dict]
    programs: dict[str, dict]


class FundedByData(APIBaseModel):
    address: str
    block_time: int
    funded_by: str
    tx_hash: str
    funded_date: datetime.datetime | None = None
    cex: str | None = ""
    dex: str | None = ""

    @model_validator(mode="after")
    def set_funded_date(self):
        from datetime import datetime

        self.funded_date = datetime.fromtimestamp(self.block_time)
        return self

    # @model_validator(mode="after")
    # def set_cex(cls, model):
    #     model.cex = CEX_ADDRESSES.get(model.funded_by, "")
    #     return model

    # @model_validator(mode="after")
    # def set_dex(cls, model):
    #     model.dex = DEX_ADDRESSES.get(model.funded_by, "")
    #     return model


class FundedByResponse(APIBaseModel):
    data: FundedByData
    metadata: MetadaBase
    success: bool

    # Serialize, only return data as dict
    @model_serializer
    def serialize(self) -> dict:
        return {
            "data": self.data,
        }
