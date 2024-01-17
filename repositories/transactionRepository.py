from typing import List
from datetime import datetime
from models.account import AccountType
from models.transaction import Transaction

class TransactionRepository:
    
    _instance = None

    def __new__(self):
        if not self._instance:
            self._instance = super().__new__(self)
            self.transactions = []
        return self._instance

    def create(self, source_user_id: str, source_account_type: str, target_user_id: str, target_account_type: str, amount: float, type: str) -> Transaction:
        new_transaction = Transaction(
            source_user_id=source_user_id,
            source_account_type=source_account_type,
            target_user_id=target_user_id,
            target_account_type=target_account_type,
            amount=amount,
            type=type,
            timestamp=datetime.now()
        )
        self.transactions.append(new_transaction)
        return new_transaction
 
    def find_by_user_id_and_account_type(self, user_id: str, account_type: AccountType) -> List[Transaction]:
        return [transaction for transaction in self.transactions if (transaction.source_user_id == user_id and transaction.source_account_type == account_type) or (transaction.target_user_id == user_id and transaction.target_account_type == account_type)]
