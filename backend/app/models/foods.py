from sqlalchemy import Column, Integer, String, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
from dependencies import Base

from models.units import Unit

class Food(Base):
    __tablename__ = "foods"
    food_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='SET NULL'), nullable=True)
    name = Column(String, nullable=False)
    brand = Column(String)
    calories = Column(DECIMAL)
    fats = Column(DECIMAL)
    saturated_fats = Column(DECIMAL)
    carbohydrates = Column(DECIMAL)
    sugars = Column(DECIMAL)
    fibers = Column(DECIMAL)
    proteins = Column(DECIMAL)
    sodium = Column(DECIMAL)
    unit_id = Column(Integer, ForeignKey('units.unit_id'), nullable=False)
    portions = relationship("Portion", back_populates="food")
    recipes = relationship("RecipeFood", back_populates="food")