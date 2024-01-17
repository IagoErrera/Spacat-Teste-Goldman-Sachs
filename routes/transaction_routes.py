from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from repositories.userRepository import UserRepository
from repositories.accountRepository import AccountRepository
from repositories.transactionRepository import TransactionRepository
from models.account import AccountType
from models.transaction import Transaction, TransferRequest, TransactionType
from dependencies import get_user_repository, get_account_repository, get_transaction_repository

transaction_router = APIRouter()

@transaction_router.get("/", response_model=list)
async def get_account_transactions(
    user_id: str,
    source_account_type: AccountType,
    user_repo: UserRepository = Depends(get_user_repository),
    transaction_repo: TransactionRepository = Depends(get_transaction_repository)
):
    user = user_repo.find_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return transaction_repo.find_by_user_id_and_account_type(user_id, source_account_type)

@transaction_router.post("/", response_model=Transaction)
async def transfer(
    source_user_id: str,
    source_account_type: str,
    transaction_request: TransferRequest,
    user_repo: UserRepository = Depends(get_user_repository),
    account_repo: AccountRepository = Depends(get_account_repository),
    transaction_repo: TransactionRepository = Depends(get_transaction_repository)
):
    source_user = user_repo.find_by_id(source_user_id)
    if source_user is None:
        raise HTTPException(status_code=404, detail="Source user not found")
    
    target_user = user_repo.find_by_id(transaction_request.target_user_id)
    if target_user is None:
        raise HTTPException(status_code=404, detail="Target user not found")

    source_account = account_repo.find_by_user_and_type(source_user_id, source_account_type)
    if source_account is None or source_account.user_id != source_user_id:
        raise HTTPException(status_code=404, detail="Source account not found")
    
    target_account = account_repo.find_by_user_and_type(transaction_request.target_user_id, transaction_request.target_account_type)
    if target_account is None or target_account.user_id != transaction_request.target_user_id:
        raise HTTPException(status_code=404, detail="Target account not found")
    
    if transaction_request.target_user_id == source_user_id and transaction_request.target_account_type == source_account_type:
        raise HTTPException(status_code=400, detail="Target account can not be the same as the source account")
    
    if transaction_request.amount < 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")

    fee_fixed, fee_relative = calculate_fees(source_user_id, transaction_request.target_user_id)

    amount_with_fees = transaction_request.amount + fee_fixed + (transaction_request.amount * fee_relative)

    if source_account.balance < transaction_request.amount:
        raise HTTPException(status_code=400, detail="Insufficient funds for transfer")
    
    source_account = account_repo.withdraw(source_user_id, source_account_type, amount_with_fees)
    target_account = account_repo.deposit(transaction_request.target_user_id, transaction_request.target_account_type, transaction_request.amount)

    transaction = transaction_repo.create(
        source_user_id=source_user_id,
        source_account_type=source_account_type,
        target_user_id=transaction_request.target_user_id,
        target_account_type=transaction_request.target_account_type,
        amount=transaction_request.amount,
        type=TransactionType.transfer_same_user if source_user_id == transaction_request.target_user_id else TransactionType.transfer_different_users
    )   
    
    return transaction.model_dump()

def calculate_fees(source_user_id: str, target_user_id: str) -> tuple[float, float]:
    # Fixed fee of 4.0 for every transaction
    # Relative fee of 1% between different users and 0.5% for different accounts of  user
    if source_user_id == target_user_id:
        return 4.0, 0.005
    else:
        return 4.0, 0.01
