import enum
from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
from dependencies import Base

class TagCategoryEnum(enum.Enum):
    PREPARATION_TIME = "Durée de préparation"
    CUISINE_TYPE = "Type de cuisine"
    DIET = "Régime alimentaire"
    SEASON = "Saison"

class Tag(Base):
    __tablename__ = "tags"
    tag_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    category = Column(Enum(TagCategoryEnum))
    recipes = relationship("Recipe", secondary="recipe_tags", back_populates="tags")
