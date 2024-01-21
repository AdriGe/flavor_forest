
from sqlalchemy import Column, Integer, String, ForeignKey, Text, Float, ARRAY, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from dependencies import Base
from models.user import User
import uuid

class Recipe(Base):
    __tablename__ = "recipes"
    recipe_id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id'))
    name = Column(String(255), nullable=False)
    headline = Column(String(255))
    description = Column(Text)
    total_time = Column(Integer)
    prep_time = Column(Integer)
    difficulty = Column(Integer)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    utensils = Column(ARRAY(String(255)))
    image_url = Column(Text)
    favorites_count = Column(Integer)
    kcal = Column(Float)
    fat = Column(Float)
    saturated_fat = Column(Float)
    carbohydrate = Column(Float)
    sugars = Column(Float)
    protein = Column(Float)
    fiber = Column(Float)
    sodium = Column(Float)
    serving_size = Column(Integer)
    steps = Column(ARRAY(Text))
    steps_images_url = Column(ARRAY(Text))

    user = relationship("User", back_populates="recipes")
    tags = relationship("Tag", secondary="recipe_tags", back_populates="recipes")
    foods = relationship("RecipeFood", back_populates="recipe")


class RecipeTag(Base):
    __tablename__ = "recipe_tags"
    recipe_id = Column(UUID(as_uuid=True), ForeignKey('recipes.recipe_id'), primary_key=True)
    tag_id = Column(UUID(as_uuid=True), ForeignKey('tags.tag_id'), primary_key=True)


class RecipeFood(Base):
    __tablename__ = "recipe_foods"
    recipe_id = Column(UUID(as_uuid=True), ForeignKey('recipes.recipe_id'), primary_key=True)
    food_id = Column(UUID(as_uuid=True), ForeignKey('foods.food_id'), primary_key=True)
    quantity = Column(Float)
    portion_id = Column(UUID(as_uuid=True), ForeignKey('portions.portion_id'))

    recipe = relationship("Recipe", back_populates="foods")
    food = relationship("Food", back_populates="recipes")
    portion = relationship("Portion")