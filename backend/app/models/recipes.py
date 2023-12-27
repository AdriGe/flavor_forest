
from sqlalchemy import Column, Integer, String, ForeignKey, Text, DECIMAL, ARRAY
from sqlalchemy.orm import relationship
from dependencies import Base
from models.user import User

class Recipe(Base):
    __tablename__ = "recipes"
    recipe_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    title = Column(String(255), nullable=False)
    description = Column(Text)
    total_time = Column(Integer)
    prep_time = Column(Integer)
    difficulty = Column(String(50))
    ustensils = Column(ARRAY(String(255)))
    image_url = Column(Text)

    user = relationship("User", back_populates="recipes")
    steps = relationship("Step", back_populates="recipe")
    tags = relationship("Tag", secondary="recipe_tags", back_populates="recipes")
    foods = relationship("RecipeFood", back_populates="recipe")


class RecipeTag(Base):
    __tablename__ = "recipe_tags"
    recipe_id = Column(Integer, ForeignKey('recipes.recipe_id'), primary_key=True)
    tag_id = Column(Integer, ForeignKey('tags.tag_id'), primary_key=True)


class RecipeFood(Base):
    __tablename__ = "recipe_foods"
    recipe_id = Column(Integer, ForeignKey('recipes.recipe_id'), primary_key=True)
    food_id = Column(Integer, ForeignKey('foods.food_id'), primary_key=True)
    quantity = Column(DECIMAL)
    portion_id = Column(Integer, ForeignKey('portions.portion_id'))

    recipe = relationship("Recipe", back_populates="foods")
    food = relationship("Food", back_populates="recipes")
    portion = relationship("Portion")