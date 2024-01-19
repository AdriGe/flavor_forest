from pydantic import BaseModel, EmailStr
import uuid

class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class UserResponse(BaseModel):
    user_id: uuid.UUID
    username: str
    email: str


class UserUpdate(BaseModel):
    email: EmailStr = None
    username: str = None
    password: str = None
