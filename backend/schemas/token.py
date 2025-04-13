from pydantic import BaseModel

class Token(BaseModel):
    """Schema for JWT tokens."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenPayload(BaseModel):
    """Schema for the data encoded within a JWT token."""
    sub: str | None = None
