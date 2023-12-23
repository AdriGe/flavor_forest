from pydantic import BaseModel
from typing import Optional, List
from schemas.portions import PortionCreate, PortionResponse

class FoodBase(BaseModel):
    name: str
    brand: Optional[str] = None
    calories: Optional[float] = None
    fats: Optional[float] = None
    saturated_fats: Optional[float] = None
    carbohydrates: Optional[float] = None
    sugars: Optional[float] = None
    fibers: Optional[float] = None
    proteins: Optional[float] = None
    sodium: Optional[float] = None
    unit_id: int

class FoodCreate(FoodBase):
    user_id: Optional[int] = None
    portions: Optional[List[PortionCreate]] = None

class FoodResponse(FoodBase):
    food_id: int
    user_id: Optional[int] = None
    portions: List[PortionResponse]

class FoodUpdate(BaseModel):
    name: Optional[str] = None
    brand: Optional[str] = None
    calories: Optional[float] = None
    fats: Optional[float] = None
    saturated_fats: Optional[float] = None
    carbohydrates: Optional[float] = None
    sugars: Optional[float] = None
    fibers: Optional[float] = None
    proteins: Optional[float] = None
    sodium: Optional[float] = None
    unit_id: Optional[int] = None
