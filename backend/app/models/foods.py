from sqlalchemy import Column, String, Float, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from dependencies import Base
import uuid

from models.units import Unit

class Food(Base):
    __tablename__ = "foods"
    food_id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id', ondelete='SET NULL'), nullable=True)
    name = Column(String, nullable=False)
    brand = Column(String)
    kcal = Column(Float)
    fat = Column(Float)
    saturated_fat = Column(Float)
    carbohydrate = Column(Float)
    sugars = Column(Float)
    fiber = Column(Float)
    protein = Column(Float)
    sodium = Column(Float)
    unit_id = Column(UUID(as_uuid=True), ForeignKey('units.unit_id'), nullable=False)
    image_url = Column(Text)
    portions = relationship("Portion", back_populates="food")
    recipes = relationship("RecipeFood", back_populates="food")
    unit = relationship("Unit", backref="foods")