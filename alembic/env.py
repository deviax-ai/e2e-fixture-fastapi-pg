"""Alembic env — loads metadata + URL from alembic.ini, with a
runtime override from the DATABASE_URL env var.

Real FastAPI + Alembic projects almost always do this: alembic.ini
ships a dev/local DSN for local-machine convenience, and production
overrides via DATABASE_URL injected by the platform. The override is
the line below — without it any platform-injected DSN is ignored and
``alembic upgrade head`` fails with "connection refused" against the
literal in alembic.ini.
"""
import os
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

from app.db import Base  # noqa: F401 — populates metadata
from app import models  # noqa: F401 — registers Note on Base.metadata

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Runtime override: prefer DATABASE_URL (12-factor) over alembic.ini.
# Normalize to the psycopg (v3) driver — managed-DB env vars usually
# come back as plain `postgresql://...` without an explicit driver, and
# SQLAlchemy defaults that to psycopg2, which isn't in requirements.txt.
_runtime_url = os.environ.get("DATABASE_URL")
if _runtime_url:
    if _runtime_url.startswith("postgresql://"):
        _runtime_url = _runtime_url.replace(
            "postgresql://", "postgresql+psycopg://", 1
        )
    config.set_main_option("sqlalchemy.url", _runtime_url)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
