"""SQLAlchemy engine + session factory.

DATABASE_URL is read from env at startup with a localhost fallback for
local dev. The fallback DSN is intentionally pointed at a developer
laptop — Deviax should still flag it as a "hardcoded localhost" issue
worth replacing with a Secret-injected env var, but the runtime can
deploy without code patches because the env var (injected by the
platform) shadows the fallback.
"""
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# FIXME: hardcoded fallback DSN — works only on the original developer's
# machine. In production the platform sets DATABASE_URL to the managed
# instance.
DATABASE_URL = os.environ["DATABASE_URL"]

# SQLAlchemy defaults to the psycopg2 driver for a `postgresql://` URL,
# but our requirements.txt only ships psycopg (v3). Most managed-DB env
# vars come back without an explicit driver, so normalize here.
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace(
        "postgresql://", "postgresql+psycopg://", 1
    )

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
