# soltradepy/infrastructure/database.py

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


def get_session() -> Session:
    """
    Devuelve una sesión nueva.
    El usuario (tú) es responsable de cerrarla al finalizar.
    """
    return Session(engine)
