from logging.config import fileConfig
from sqlalchemy import engine_from_config, create_engine, pool
from alembic import context
from db.base import Base  # your models Base
from dotenv import load_dotenv
import os

load_dotenv()

config = context.config

# Inject .env DB URL if not hardcoded
config.set_main_option("sqlalchemy.url", os.getenv("DATABASE_URL_SYNC"))  # sync version!

fileConfig(config.config_file_name)
target_metadata = Base.metadata

def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True, dialect_opts={"paramstyle": "named"}
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = create_engine(  # <-- sync engine
        config.get_main_option("sqlalchemy.url"),
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
