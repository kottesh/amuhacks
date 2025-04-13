from pydantic import BaseModel, Field
from typing import Optional

class AccountBase(BaseModel):
    """Base schema for financial accounts."""
    name: str = Field(..., description="Name of the account (e.g., 'HDFC Savings', 'Cash Wallet')")
    type: str = Field(..., description="Type of account (e.g., 'Bank', 'Credit Card', 'Cash', 'Investment')")
    balance: float = Field(default=0.0, description="Current balance of the account")

    model_config = {
        "from_attributes": True
    }

class AccountCreate(AccountBase):
    """Schema for creating a new account."""
    pass

class AccountUpdate(BaseModel):
    """Schema for updating an account (all fields optional)."""
    name: str | None = None
    type: str | None = None
    balance: float | None = None

class Account(AccountBase):
    """Schema representing an account returned by the API."""
    id: int
    owner_id: int
