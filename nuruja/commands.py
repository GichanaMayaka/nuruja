import click
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Engine
from sqlalchemy_utils import create_database, database_exists, drop_database

from .extensions import db
from ..configs import configs


def database_engine(uri: str) -> Engine:
    engine = create_engine(uri)
    return engine


def create_db(uri: str = configs.POSTGRES_DSN) -> None:
    engine = database_engine(uri)

    if not database_exists(engine.url):
        create_database(engine.url)


def drop_db() -> None:
    if click.confirm("Are you sure?", default=False, abort=True):
        engine = database_engine(uri=configs.POSTGRES_DSN)
        if database_exists(engine.url):
            drop_database(engine.url)


def create_tables(database: SQLAlchemy = db) -> None:
    """Create all tables defined in the model[s]"""
    database.create_all()


def drop_tables() -> None:
    """Drops tables."""
    if click.confirm("Are you sure?", default=False, abort=True):
        db.drop_all()


def recreate_tables() -> None:
    """Same as running drop_tables() and create_tables()."""
    drop_tables()
    create_tables()
