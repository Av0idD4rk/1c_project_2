# app/models/exhibition.py

from sqlalchemy import Column, Integer, String, Text
from app.database import Base

class Exhibition(Base):
    __tablename__ = "exhibitions"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)

    # 1:1 к Order (см. order.py)
