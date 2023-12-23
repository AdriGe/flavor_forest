from pydantic import BaseModel
from typing import Optional

class PortionCreate(BaseModel):
    name: str
    size: float

class PortionResponse(BaseModel):
    portion_id: int
    food_id: int
    name: str
    size: float

class PortionUpdate(BaseModel):
    name: Optional[str] = None
    size: Optional[float] = None