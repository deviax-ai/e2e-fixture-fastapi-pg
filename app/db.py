"""SQLAlchemy engine + session factory.

NOTE — DATABASE_URL is hardcoded for local dev. In production this
should come from the environment.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# FIXME: hardcoded DSN — works only on the original developer's
# machine. Replace with `os.environ["DATABASE_URL"]` before deploying.
DATABASE_URL = "postgresql+psycopg://postgres:postgres@localhost:5432/notes"

engine = create_engine(DATABASE_URL, pool_pre_ping=True, future=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


class Base(DeclarativeBase):
    """SQLAlchemy 2.0 declarative base."""


def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
