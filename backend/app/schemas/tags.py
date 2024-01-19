from pydantic import BaseModel
from enum import Enum
from typing import Optional
import uuid

class TagCategoryEnum(str, Enum):
    CULINARY_STYLE = "culinary_style"
    DIETARY_REGIME = "dietary_regime"
    MEAL_TYPE = "meal_type"

class TagDetail(BaseModel):
    tag_id: uuid.UUID
    name: str
    category: TagCategoryEnum

class TagCreate(BaseModel):
    name: str
    category: TagCategoryEnum

class TagUpdate(BaseModel):
    name: str
    category: Optional[TagCategoryEnum] = None
