from pydantic import BaseModel
from typing import Optional, List
from schemas.portions import PortionCreate, PortionResponse, PortionDetail
import uuid

class FoodBase(BaseModel):
    name: str
    brand: Optional[str] = None
    kcal: Optional[float] = None
    fat: Optional[float] = None
    saturated_fat: Optional[float] = None
    carbohydrate: Optional[float] = None
    sugars: Optional[float] = None
    fiber: Optional[float] = None
    protein: Optional[float] = None
    sodium: Optional[float] = None
    unit_id: uuid.UUID

class FoodCreate(FoodBase):
    user_id: Optional[uuid.UUID] = None
    portions: Optional[List[PortionCreate]] = None

class FoodResponse(FoodBase):
    food_id: uuid.UUID
    user_id: Optional[uuid.UUID] = None
    portions: List[PortionResponse]

class FoodUpdate(BaseModel):
    name: Optional[str] = None
    brand: Optional[str] = None
    kcal: Optional[float] = None
    fat: Optional[float] = None
    saturated_fat: Optional[float] = None
    carbohydrate: Optional[float] = None
    sugars: Optional[float] = None
    fiber: Optional[float] = None
    protein: Optional[float] = None
    sodium: Optional[float] = None
    unit_id: Optional[uuid.UUID] = None

class FoodDetail(BaseModel):
    food_id: uuid.UUID
    name: str
    brand: Optional[str] = None
    kcal: Optional[float] = None
    fat: Optional[float] = None
    saturated_fat: Optional[float] = None
    carbohydrate: Optional[float] = None
    sugars: Optional[float] = None
    fiber: Optional[float] = None
    protein: Optional[float] = None
    sodium: Optional[float] = None
    unit_id: uuid.UUID
    portions: List[PortionDetail]

class FoodListResponse(BaseModel):
    total_foods: int
    total_pages: int
    foods: List[FoodDetail]
