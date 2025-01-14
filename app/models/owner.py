
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class Owner(Base):
    __tablename__ = "owners"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    exhibits = relationship("Exhibit", back_populates="owner")
