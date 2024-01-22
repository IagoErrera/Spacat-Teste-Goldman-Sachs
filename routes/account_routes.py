from fastapi import APIRouter, HTTPException, Depends
from repositories.userRepository import UserRepository
from repositories.accountRepository import AccountRepository
from repositories.transactionRepository import TransactionRepository
from models.account import Account, AccountRequest, AccountType
from models.transaction import SameAccountTransactionRequest, TransactionType
from dependencies import get_user_repository, get_account_repository, get_transaction_repository

account_router = APIRouter()

@account_router.post("/{account_type}", response_model=Account)
async def create_account(
    user_id: str,
    account_type: AccountType,
    account_data: AccountRequest,
    user_repo: UserRepository = Depends(get_user_repository),
    account_repo: AccountRepository = Depends(get_account_repository)
):
    user = user_repo.find_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    existing_account = account_repo.find_by_user_and_type(user_id, account_type)
    print(existing_account)
    if existing_account:
        raise HTTPException(status_code=400, detail="Account with the same type already exists for the user")
    
    if account_data.balance < 0:
        raise HTTPException(status_code=400, detail="Account balance must be positive")

    new_account = account_repo.create(user_id, account_type, account_data)

    return new_account.model_dump()

@account_router.get("/", response_model=list)
async def get_user_accounts(
    user_id: str,
    user_repo: UserRepository = Depends(get_user_repository),
    account_repo: AccountRepository = Depends(get_account_repository)
):
    user = user_repo.find_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return account_repo.find_by_user_id(user_id)

@account_router.put("/{account_type}/deposit", response_model=Account)
async def deposit(
    user_id: str,
    account_type: AccountType,
    transaction_request: SameAccountTransactionRequest,
    user_repo: UserRepository = Depends(get_user_repository),
    transaction_repo: TransactionRepository = Depends(get_transaction_repository),
    account_repo: AccountRepository = Depends(get_account_repository),
):
    user = user_repo.find_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    account = account_repo.find_by_user_and_type(user_id, account_type)
    if account is None or account.user_id != user_id:
        raise HTTPException(status_code=404, detail="Account not found")
    
    if transaction_request.amount < 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")
    
    updated_account = account_repo.deposit(user_id, account_type, transaction_request.amount)
    transaction = transaction_repo.create(
        source_user_id=user_id,
        source_account_type=account_type,
        target_user_id=user_id,
        target_account_type=account_type,
        amount=transaction_request.amount,
        type=TransactionType.deposit,
    )

    transaction.model_dump()
    return updated_account.model_dump()

@account_router.put("/{account_type}/withdraw", response_model=Account)
async def withdraw(
    user_id: str,
    account_type: AccountType,
    transaction_request: SameAccountTransactionRequest,
    user_repo: UserRepository = Depends(get_user_repository),
    transaction_repo: TransactionRepository = Depends(get_transaction_repository),
    account_repo: AccountRepository = Depends(get_account_repository),    
):
    user = user_repo.find_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    account = account_repo.find_by_user_and_type(user_id, account_type)
    if account is None or account.user_id != user_id:
        raise HTTPException(status_code=404, detail="Account not found")
    
    if account.balance < transaction_request.amount or (account.balance - transaction_request.amount) < 0:
        raise HTTPException(status_code=400, detail="Insufficient funds")
    
    if transaction_request.amount < 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")

    updated_account = account_repo.withdraw(user_id, account_type, transaction_request.amount)
    transaction = transaction_repo.create(
        source_user_id=user_id,
        source_account_type=account_type,
        target_user_id=user_id,
        target_account_type=account_type,
        amount=transaction_request.amount,
        type=TransactionType.withdraw,
    )

    transaction.model_dump()
    return updated_account.model_dump()
