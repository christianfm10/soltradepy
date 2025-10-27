# tests/conftest.py
import pytest
from sqlmodel import SQLModel, Session, create_engine

# from soltradepy.storage.graduated_tokens_store import GraduatedTokensSQLStore
from soltradepy.storage import graduated_tokens_store


@pytest.fixture
def test_session():
    engine = create_engine("sqlite:///:memory:", echo=False)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


""" @pytest.fixture
def store(test_session):
    return GraduatedTokensSQLStore(session=test_session)
 """


@pytest.fixture
def in_memory_db(monkeypatch):
    engine = create_engine("sqlite:///:memory:", echo=False)
    SQLModel.metadata.create_all(engine)

    def _override_get_session():
        return Session(engine)

    # monkeypatch.setattr(
    #     "soltradepy.storage.graduated_tokens_store.get_session", _override_get_session
    # )
    monkeypatch.setattr(graduated_tokens_store, "get_session", _override_get_session)
    yield engine


# Moralis Client fixture
@pytest.fixture
def moralis_client():
    from soltradepy.infrastructure.data_providers.moralis.moralis_client import (
        MoralisClient,
    )
    from soltradepy.infrastructure.config.env import settings

    return MoralisClient(settings.moralis_api_key)
