import datetime
import json

from sqlmodel import Field, SQLModel


class BaseWallet(SQLModel):
    public_key: str = Field(index=True, unique=True)
    balance: int | None = None  # lamports


class UserWallet(BaseWallet, table=True):
    __tablename__ = "user_wallets"  # type: ignore
    id: int | None = Field(
        default=None,
        primary_key=True,
    )

    funded_wallet: str | None = None
    funded_txn: str | None = None
    funded_date: datetime.datetime | None = None
    funded_amount: int | None = None

    created_tokens_count: int | None = None
    has_usdc: bool | None = None
    is_isma: bool = False

    tags_json: str | None = Field(
        default="[]"
    )  # Use tags property instead of tags_json

    def __init__(self, **data):
        tags = data.pop("tags", None)
        super().__init__(**data)
        if tags is not None:
            self.tags = tags

    @classmethod
    def from_user_created_coins(cls, data: dict):
        key_map = {
            "public_key": "public_key",
            "count": "created_tokens_count",
        }
        mapped_data = {key_map[k]: v for k, v in data.items() if k in key_map}

        return cls(**mapped_data)

    @classmethod
    def from_funded_by(cls, data: dict):
        key_map = {
            "address": "public_key",
            "funded_by": "funded_wallet",
            "tx_hash": "funded_txn",
            "funded_date": "funded_date",
        }
        mapped_data = {key_map[k]: v for k, v in data.items() if k in key_map}

        return cls(**mapped_data)

    @property
    def tags(self) -> list[str]:
        return json.loads(self.tags_json or "[]")

    @tags.setter
    def tags(self, value: list[str]):
        self.tags_json = json.dumps(value)
