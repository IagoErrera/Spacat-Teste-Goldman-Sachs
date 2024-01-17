from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum
import uuid

class AccountType(str, Enum):
    savings = "savings"
    current = "current"
    investments = "investments"

class AccountRequest(BaseModel):
    balance: float = 0.0

class Account(BaseModel):
    account_type: AccountType
    user_id: str
    balance: float = 0.0
    lastUpdated: datetime = Field(default_factory=datetime.now)
