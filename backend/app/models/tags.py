import enum
from sqlalchemy import Column, String, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from dependencies import Base
import uuid

class TagCategoryEnum(enum.Enum):
    culinary_style = "culinary_style"
    dietary_regime = "dietary_regime"
    meal_type = "meal_type"

class Tag(Base):
    __tablename__ = "tags"
    tag_id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    category = Column(Enum(TagCategoryEnum), nullable=False)
    recipes = relationship("Recipe", secondary="recipe_tags", back_populates="tags")
