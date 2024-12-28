# app/models/exhibit.py

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Exhibit(Base):
    __tablename__ = "exhibits"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    owner_id = Column(Integer, ForeignKey("owners.id"), nullable=False)
    owner = relationship("Owner", back_populates="exhibits")

    # Связи M:N
    orders = relationship(
        "Order",
        secondary="order_exhibit_association",
        back_populates="exhibits"
    )

    arrivals = relationship(
        "ArrivalAct",
        secondary="arrival_exhibit_association",
        back_populates="exhibits"
    )

    transfers = relationship(
        "TransferAct",
        secondary="transfer_exhibit_association",
        back_populates="exhibits"
    )

    returns = relationship(
        "ReturnAct",
        secondary="return_exhibit_association",
        back_populates="exhibits"
    )
