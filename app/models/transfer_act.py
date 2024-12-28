# app/models/transfer_act.py

from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base
from app.models.association_tables import transfer_exhibit_association

class TransferAct(Base):
    __tablename__ = "transfer_acts"

    id = Column(Integer, primary_key=True, index=True)

    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    transferred_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    exhibits = relationship(
        "Exhibit",
        secondary=transfer_exhibit_association,
        back_populates="transfers"
    )
