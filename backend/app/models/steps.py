
from sqlalchemy import Column, Integer, ForeignKey, Text, ARRAY
from sqlalchemy.orm import relationship
from dependencies import Base

    
class Step(Base):
    __tablename__ = "steps"
    step_number = Column(Integer, primary_key=True, index=True)
    recipe_id = Column(Integer, ForeignKey('recipes.recipe_id'), primary_key=True)
    description = Column(ARRAY(Text))
    image_url = Column(Text)

    recipe = relationship("Recipe", back_populates="steps")
