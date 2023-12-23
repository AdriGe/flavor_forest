from sqlalchemy import Column, Integer, String
from dependencies import Base

class Unit(Base):
    __tablename__ = "units"
    unit_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)