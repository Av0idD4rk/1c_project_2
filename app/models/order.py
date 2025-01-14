
from sqlalchemy import Column, Integer, DateTime, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base
from app.models.association_tables import order_exhibit_association

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)

    exhibition_id = Column(Integer, ForeignKey("exhibitions.id"), nullable=False)
    exhibition = relationship("Exhibition", backref="order", uselist=False)

    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)

    venue = Column(String, nullable=True)

    exhibits = relationship(
        "Exhibit",
        secondary=order_exhibit_association,
        back_populates="orders"
    )
