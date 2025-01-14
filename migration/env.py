import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

config = context.config

fileConfig(config.config_file_name)

from app.database import Base
from app.models.owner import Owner
from app.models.exhibit import Exhibit
from app.models.exhibition import Exhibition
from app.models.order import Order
from app.models.arrival_act import ArrivalAct
from app.models.transfer_act import TransferAct
from app.models.return_act import ReturnAct
from app.models.association_tables import (
    order_exhibit_association,
    arrival_exhibit_association,
    transfer_exhibit_association,
    return_exhibit_association,
)

target_metadata = Base.metadata

def run_migrations_offline():
    url = "postgresql://postgres:postgres@db:5432/main"
    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True, dialect_opts={"paramstyle": "named"}
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    ini_section = config.get_section(config.config_ini_section)
    connectable = engine_from_config(
        ini_section,
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
