from typing import List
from datetime import datetime
from models.account import Account, AccountType, AccountRequest

class AccountRepository:

    _instance = None

    def __new__(self):
        if not self._instance:
            self._instance = super().__new__(self)
            self.accounts = []
        return self._instance

    def create(self, user_id: str, account_type: AccountType, account_data: AccountRequest) -> Account:
        if account_data.balance < 0:
            raise ValueError("Balance must be positive")

        new_account = Account(user_id=user_id, account_type=account_type, **account_data.model_dump(), lastUpdated=datetime.now())
        self.accounts.append(new_account)
        return new_account

    def find_by_user_and_type(self, user_id: str, account_type: str) -> Account:
        return next((account for account in self.accounts if account.user_id == user_id and account.account_type == account_type), None)

    def find_by_user_id(self, user_id: str) -> List[Account]:
        return [account for account in self.accounts if account.user_id == user_id]

    def deposit(self, user_id: str, account_type: str, amount: float) -> Account:
        account = self.find_by_user_and_type(user_id, account_type)
        if account:
            account.balance += amount
            account.lastUpdated = datetime.now()
        return account

    def withdraw(self,user_id: str, account_type: str, amount: float) -> Account:
        account = self.find_by_user_and_type(user_id, account_type)
        if account:
            account.balance -= amount
            account.lastUpdated = datetime.now()
        return account
