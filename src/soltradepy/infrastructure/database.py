# soltradepy/infrastructure/database.py


# from typing import Generator, Iterator
from collections.abc import Iterator
from contextlib import contextmanager

from sqlmodel import Session, SQLModel, create_engine

from soltradepy.infrastructure.config.env import get_settings

settings = get_settings()
engine = create_engine(
    settings.database_url,
    echo=settings.debug_sql,  # pon True si deseas ver SQL en consola para debug
)
""" def create_engine_from_settings():
    settings = get_settings()
    return create_engine(
        settings.database_url,
        echo=settings.debug_sql,
    )
 """


def init_db() -> None:
    """Crea las tablas si no existen (solo se ejecuta una vez al inicio del proyecto)."""
    SQLModel.metadata.create_all(engine)


# @contextmanager
def get_session():
    """
    Devuelve una sesión nueva.
    El usuario (tú) es responsable de cerrarla al finalizar.
    """
    # engine = create_engine_from_settings()

    # with Session(engine) as session:
    #     yield session
    # session = Session(engine)
    return Session(engine)
