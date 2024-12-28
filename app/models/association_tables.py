# app/models/association_tables.py

from sqlalchemy import Table, Column, Integer, ForeignKey
from app.database import Base

order_exhibit_association = Table(
    "order_exhibit_association",
    Base.metadata,
    Column("order_id", Integer, ForeignKey("orders.id"), primary_key=True),
    Column("exhibit_id", Integer, ForeignKey("exhibits.id"), primary_key=True),
)

arrival_exhibit_association = Table(
    "arrival_exhibit_association",
    Base.metadata,
    Column("arrival_act_id", Integer, ForeignKey("arrival_acts.id"), primary_key=True),
    Column("exhibit_id", Integer, ForeignKey("exhibits.id"), primary_key=True),
)

transfer_exhibit_association = Table(
    "transfer_exhibit_association",
    Base.metadata,
    Column("transfer_act_id", Integer, ForeignKey("transfer_acts.id"), primary_key=True),
    Column("exhibit_id", Integer, ForeignKey("exhibits.id"), primary_key=True),
)

return_exhibit_association = Table(
    "return_exhibit_association",
    Base.metadata,
    Column("return_act_id", Integer, ForeignKey("return_acts.id"), primary_key=True),
    Column("exhibit_id", Integer, ForeignKey("exhibits.id"), primary_key=True),
)
