# models.py
from sqlalchemy import Column, Integer, ForeignKey, DECIMAL, String
from sqlalchemy.orm import relationship
from dependencies import Base

class Portion(Base):
    __tablename__ = "portions"
    portion_id = Column(Integer, primary_key=True, index=True)
    food_id = Column(Integer, ForeignKey('foods.food_id'), nullable=False)
    name = Column(String)
    size = Column(DECIMAL, nullable=False)

    food = relationship("Food", back_populates="portions")

