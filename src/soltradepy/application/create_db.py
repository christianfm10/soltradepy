# Init DB
# WARNING: Dont Remove
import soltradepy.domain
import soltradepy.infrastructure.database as db


def create_database():
    """Crea la base de datos y las tablas necesarias."""
    db.init_db()


def cli():
    create_database()
    print("Database and tables created successfully.")
