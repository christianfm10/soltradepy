# Init DB
from soltradepy.infrastructure.database import init_db

import soltradepy.infrastructure.database as db
import soltradepy.domain


def create_database():
    """Crea la base de datos y las tablas necesarias."""
    db.init_db()


def cli():
    create_database()
    print("Database and tables created successfully.")
