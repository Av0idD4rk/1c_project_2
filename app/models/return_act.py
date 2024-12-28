# app/models/return_act.py

from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base
from app.models.association_tables import return_exhibit_association

class ReturnAct(Base):
    __tablename__ = "return_acts"

    id = Column(Integer, primary_key=True, index=True)

    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    returned_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    exhibits = relationship(
        "Exhibit",
        secondary=return_exhibit_association,
        back_populates="returns"
    )
