import asyncio
import os
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context

# Import your Base and models so Alembic can see them
# IMPORTANT: Adjust the import path to match your project
from backend.db.models import Base
from backend.db.session import db_url  # or import DATABASE_URL directly

# This is the Alembic Config object
config = context.config

# Set the database URL from your existing config
# (Don't hardcode it - read from where you already store it)
config.set_main_option("sqlalchemy.url", db_url)  # or os.getenv("DATABASE_URL")

# Setup logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# THIS IS CRITICAL - Alembic needs your models' metadata
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    """Synchronous migration runner - called by async version."""
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """Run migrations in 'online' mode with async engine."""
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)


def run_migrations_online() -> None:
    """Run migrations in 'online' mode - entry point for async."""
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()