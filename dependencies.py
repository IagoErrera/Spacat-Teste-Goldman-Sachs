from fastapi import Depends
from repositories.userRepository import UserRepository
from repositories.accountRepository import AccountRepository
from repositories.transactionRepository import TransactionRepository

def get_user_repository() -> UserRepository:
    return UserRepository()

def get_account_repository() -> AccountRepository:
    return AccountRepository()

def get_transaction_repository() -> TransactionRepository:
    return TransactionRepository()
