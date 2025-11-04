# tests/conftest.py
import pytest
from sqlmodel import Session, SQLModel, create_engine


@pytest.fixture(autouse=True, scope="function")
def use_test_db():
    """Usa una base SQLite en memoria para cada test."""
    import soltradepy.domain

    engine = create_engine(
        "sqlite:///temporal.db", connect_args={"check_same_thread": False}
    )

    SQLModel.metadata.create_all(engine)
    yield engine
    SQLModel.metadata.drop_all(engine)


@pytest.fixture
def session(use_test_db):
    """Fixture para obtener una sesión de base de datos para tests."""
    with Session(use_test_db) as session:
        yield session
    return


@pytest.fixture(autouse=True)
def settings():
    """Fixture to reset settings before each test."""
    from soltradepy.infrastructure.config.env import get_settings

    get_settings.cache_clear()
    settings = get_settings()
    yield settings
    get_settings.cache_clear()


# @pytest.fixture
# def in_memory_db(monkeypatch):
#     engine = create_engine("sqlite:///:memory:", echo=False)
#     SQLModel.metadata.create_all(engine)

#     @contextmanager
#     def _override_get_session():
#         session = Session(engine)
#         try:
#             yield session
#             session.commit()
#         except:
#             session.rollback()
#             raise
#         finally:
#             session.close()

#     # monkeypatch.setattr(
#     #     "soltradepy.storage.graduated_tokens_store.get_session", _override_get_session
#     # )
#     monkeypatch.setattr(graduated_tokens_store, "get_session", _override_get_session)
#     yield engine


@pytest.fixture
def moralis_client(settings):
    """Fixture for MoralisClient instance."""
    from soltradepy.infrastructure.data_providers.moralis.moralis_client import (
        MoralisClient,
    )

    return MoralisClient(settings.moralis_api_key)


@pytest.fixture
def pumpfun_client():
    """Fixture for PumpfunClient instance."""
    from soltradepy.infrastructure.data_providers.pumpfun.pumpfun_client import (
        PumpfunClient,
    )

    return PumpfunClient()
