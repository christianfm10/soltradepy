# soltradepy/infrastructure/database.py

from contextlib import contextmanager
from typing import Generator
from sqlmodel import SQLModel, create_engine, Session
from soltradepy.infrastructure.config.env import settings

# DATABASE_URL = "sqlite:///./soltradepy.db"  # luego puedes cambiar a postgresql://...
# DATABASE_URL = "sqlite:///:memory:"  # luego puedes cambiar a postgresql://...


engine = create_engine(
    settings.database_url,
    echo=settings.debug_sql,  # pon True si deseas ver SQL en consola para debug
)


def init_db() -> None:
    """Crea las tablas si no existen (solo se ejecuta una vez al inicio del proyecto)."""
    SQLModel.metadata.create_all(engine)


@contextmanager
def get_session() -> Generator:
    """
    Devuelve una sesión nueva.
    El usuario (tú) es responsable de cerrarla al finalizar.
    """
    session = Session(engine)
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
