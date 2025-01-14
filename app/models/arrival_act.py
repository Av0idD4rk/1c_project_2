
from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base
from app.models.association_tables import arrival_exhibit_association

class ArrivalAct(Base):
    __tablename__ = "arrival_acts"

    id = Column(Integer, primary_key=True, index=True)

    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    arrived_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    exhibits = relationship(
        "Exhibit",
        secondary=arrival_exhibit_association,
        back_populates="arrivals"
    )
