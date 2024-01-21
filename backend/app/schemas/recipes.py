from pydantic import BaseModel
from typing import List, Optional, Union
from schemas.tags import TagDetail
import uuid
from datetime import datetime

class RecipeFoodCreate(BaseModel):
    food_id: uuid.UUID
    quantity: float
    portion_id: Optional[uuid.UUID] = None


class RecipeCreate(BaseModel):
    name: str
    headline: Optional[str] = None
    description: Optional[str] = None
    total_time: Optional[int] = None
    prep_time: Optional[int] = None
    difficulty: Optional[int] = None
    utensils: Optional[List[str]] = None
    image_url: Optional[str] = None
    kcal: Optional[int] = None
    fat: Optional[float] = None
    saturated_fat: Optional[float] = None
    carbohydrate: Optional[float] = None
    sugars: Optional[float] = None
    protein: Optional[float] = None
    fiber: Optional[float] = None
    sodium: Optional[float] = None
    steps: List[str]
    steps_images_url: List[str]
    tags: List[uuid.UUID]
    foods: List[RecipeFoodCreate]


class RecipeFoodDetail(BaseModel):
    food_id: uuid.UUID
    food_name: str
    quantity: Optional[float] = None
    portion_id: Optional[uuid.UUID] = None
    unit: str


class RecipeDetail(BaseModel):
    recipe_id: uuid.UUID
    user_id: Union[uuid.UUID, None]
    name: str
    headline: Optional[str]
    description: Optional[str]
    total_time: Optional[int]
    prep_time: Optional[int]
    difficulty: Optional[int]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    utensils: Optional[List[str]]
    image_url: Optional[str]
    favorites_count: Optional[int]
    kcal: Optional[int]
    fat: Optional[float]
    saturated_fat: Optional[float]
    carbohydrate: Optional[float]
    sugars: Optional[float]
    protein: Optional[float]
    fiber: Optional[float]
    sodium: Optional[float]
    serving_size: Optional[int]
    steps: List[str]
    steps_images_url: List[str]
    foods: List[RecipeFoodDetail]
    tags: List[TagDetail]


class RecipeUpdate(BaseModel):
    user_id: Optional[uuid.UUID] = None
    name: Optional[str] = None
    headline: Optional[str] = None
    description: Optional[str] = None
    total_time: Optional[int] = None
    prep_time: Optional[int] = None
    difficulty: Optional[int] = None
    utensils: Optional[List[str]] = None
    image_url: Optional[str] = None
    favorites_count: Optional[int] = None
    kcal: Optional[int] = None
    fat: Optional[float] = None
    saturated_fat: Optional[float] = None
    carbohydrate: Optional[float] = None
    sugars: Optional[float] = None
    protein: Optional[float] = None
    fiber: Optional[float] = None
    sodium: Optional[float] = None
    steps: Optional[List[str]] = None
    steps_images_url: Optional[List[str]] = None
    foods: Optional[List[RecipeFoodDetail]] = None
    tags: Optional[List[uuid.UUID]] = None


class RecipeTagsUpdate(BaseModel):
    tags: List[uuid.UUID]


class RecipeListResponse(BaseModel):
    total_recipes: int
    total_pages: int
    recipes: List[RecipeDetail]