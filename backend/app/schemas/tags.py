from pydantic import BaseModel

class TagDetail(BaseModel):
    tag_id: int
    name: str

class TagCreate(BaseModel):
    name: str

class TagUpdate(BaseModel):
    name: str
