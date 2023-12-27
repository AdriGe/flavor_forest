
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from dependencies import Base


class Tag(Base):
    __tablename__ = "tags"
    tag_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    recipes = relationship("Recipe", secondary="recipe_tags", back_populates="tags")
