from pydantic import BaseModel, EmailStr, validator, ValidationError
import uuid

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

    @validator('password')
    def password_complexity(cls, v):
        # Minimum 8 characters in length
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')

        # Check for other complexity requirements as needed
        # Example: At least one uppercase, one lowercase, one digit, and one special character
        if not any(char.isupper() for char in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(char.islower() for char in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(char.isdigit() for char in v):
            raise ValueError('Password must contain at least one digit')
        if not any(char in "!@#$%^&*()_+" for char in v):
            raise ValueError('Password must contain at least one special character !@#$%^&*()_+')

        return v


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class UserResponse(BaseModel):
    user_id: uuid.UUID
    username: str
    email: EmailStr

