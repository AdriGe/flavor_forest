from pydantic import BaseModel
from typing import List, Optional
from schemas.tags import TagDetail


class StepCreate(BaseModel):
    step_number: int
    description: List[str]


class RecipeFoodCreate(BaseModel):
    food_id: int
    quantity: float
    portion_id: Optional[int] = None


class RecipeCreate(BaseModel):
    title: str
    description: Optional[str] = None
    total_time: Optional[int] = None
    prep_time: Optional[int] = None
    difficulty: Optional[str] = None
    ustensils: Optional[List[str]] = None
    image_url: Optional[str] = None
    user_id: Optional[int] = None
    steps: List[StepCreate]
    tags: List[int]
    foods: List[RecipeFoodCreate]


class StepDetail(BaseModel):
    step_number: int
    description: List[str]
    image_url: Optional[str] = None


class RecipeFoodDetail(BaseModel):
    food_id: int
    food_name: str
    quantity: float
    measurement: str


class RecipeDetail(BaseModel):
    recipe_id: int
    user_id: int
    title: str
    description: Optional[str]
    total_time: Optional[int]
    prep_time: Optional[int]
    difficulty: Optional[str]
    ustensils: Optional[List[str]]
    image_url: Optional[str]
    steps: List[StepDetail]
    foods: List[RecipeFoodDetail]
    tags: List[TagDetail]


class RecipeUpdate(BaseModel):
    user_id: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    total_time: Optional[int] = None
    prep_time: Optional[int] = None
    difficulty: Optional[str] = None
    ustensils: Optional[List[str]] = None
    image_url: Optional[str] = None

class RecipeTagsUpdate(BaseModel):
    tags: List[int]


class StepUpdate(BaseModel):
    step_number: int
    description: List[str]
    image_url: Optional[str] = None


class RecipeStepsUpdate(BaseModel):
    steps: List[StepUpdate]


class RecipeListResponse(BaseModel):
    total_recipes: int
    total_pages: int
    recipes: List[RecipeDetail]