from datetime import datetime, timezone
from pydantic import BaseModel, Field, validator
from enum import Enum

class TransactionType(str, Enum):
    """Enum for transaction types."""
    INCOME = 'INCOME'
    EXPENSE = 'EXPENSE'
    TRANSFER = 'TRANSFER'

class TransactionBase(BaseModel):
    """Base schema for transactions."""
    amount: float = Field(..., gt=0, description="Transaction amount (must be positive)")
    category: str | None = Field(None, description="Category of the transaction (e.g., 'Groceries', 'Salary')")
    description: str | None = Field(None, description="Optional description of the transaction")
    date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="Date and time of the transaction")
    account_id: int = Field(..., description="ID of the account associated with this transaction")

    model_config = {
        "from_attributes": True,
        "use_enum_values": True
    }

class TransactionCreate(TransactionBase):
    """Schema for creating a new transaction."""
    type: TransactionType = Field(..., description="Type of transaction (INCOME or EXPENSE)")

class TransactionUpdate(BaseModel):
    """Schema for updating a transaction (all fields optional)."""
    amount: float | None = Field(None, gt=0)
    category: str | None = None
    description: str | None = None
    date: datetime | None = None
    type: TransactionType | None = None
    account_id: int | None = None

class Transaction(TransactionBase):
    """Schema representing a transaction returned by the API."""
    id: int
    type: TransactionType
    owner_id: int

class NlpInput(BaseModel):
    """Schema for the input text for NLP parsing."""
    text: str = Field(..., description="Natural language text describing the transaction(s)")

class NlpParsedTransaction(BaseModel):
    """
    Schema matching the expected JSON structure from the LLM.
    This is used for the /parse endpoint response before final confirmation.
    """
    amount: float = Field(..., gt=0)
    category: str | None = None
    type: TransactionType
    description: str | None = None
    date: datetime | None = None

    @validator('category', pre=True, always=True)
    def set_default_category(cls, v, values):
        """Set default category based on type if LLM omits it."""
        if v is None or v == "":
            type_val = values.get('type')
            if type_val == TransactionType.INCOME:
                return "Other Income"
            elif type_val == TransactionType.EXPENSE:
                return "Other Expense"
        return v
