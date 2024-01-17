from pydantic import BaseModel, Field
from datetime import datetime
from models.account import AccountType
from enum import Enum
import uuid

class TransactionType(str, Enum):
    deposit = "deposit"
    withdraw = "withdraw"
    transfer_same_user = "transfer_same_user"
    transfer_different_users = "transfer_different_users"
    payment = "payment"

class Transaction(BaseModel):
    transaction_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    source_user_id: str
    source_account_type: AccountType
    target_user_id: str
    target_account_type: AccountType
    amount: float
    type: TransactionType
    timestamp: datetime = Field(default_factory=datetime.now)

class TransferRequest(BaseModel):
    target_user_id: str
    target_account_type: AccountType
    amount: float
    
class SameAccountTransactionRequest(BaseModel):
    amount: float