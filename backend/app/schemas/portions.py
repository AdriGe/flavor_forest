from pydantic import BaseModel
from typing import Optional
import uuid

class PortionCreate(BaseModel):
    name: str
    size: float

class PortionResponse(BaseModel):
    portion_id: uuid.UUID
    food_id: int
    name: str
    size: float

class PortionUpdate(BaseModel):
    name: Optional[str] = None
    size: Optional[float] = None
    
class PortionDetail(BaseModel):
    portion_id: uuid.UUID
    name: str
    size: float