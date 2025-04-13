from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserBase(BaseModel):
    """Base user schema with common fields."""
    first_name: str
    last_name: str | None
    email: EmailStr = Field(..., description="User's unique email address")
    is_active: bool | None = True

    model_config  = {
        "from_attributes": True
    }

class UserCreate(UserBase):
    """Schema used when creating a new user."""
    password: str = Field(..., min_length=8, description="User's password (min 8 characters)")

class UserUpdate(UserBase):
    """Schema used when updating an existing user (optional fields)."""
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None
    password: str | None = None
    is_active: bool | None = None

class UserInDBBase(UserBase):
    """Schema representing a user as stored in the database."""
    id: int
    hashed_password: str

class User(UserBase):
    """Schema representing a user returned by the API (no password)."""
    id: int
