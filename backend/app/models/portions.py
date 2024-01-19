# models.py
from sqlalchemy import Column, ForeignKey, Float, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from dependencies import Base
import uuid

class Portion(Base):
    __tablename__ = "portions"
    portion_id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    food_id = Column(UUID(as_uuid=True), ForeignKey('foods.food_id'), nullable=False)
    name = Column(String)
    size = Column(Float, nullable=False)

    food = relationship("Food", back_populates="portions")

