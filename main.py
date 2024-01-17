from fastapi import FastAPI
from routes.user_routes import user_router
from routes.account_routes import account_router
from routes.transaction_routes import transaction_router
from dependencies import get_user_repository, get_account_repository, get_transaction_repository

app = FastAPI()

user_repository = get_user_repository()
account_repository = get_account_repository()
transaction_repository = get_transaction_repository()

app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(account_router, prefix="/users/{user_id}/accounts", tags=["accounts"])
app.include_router(transaction_router, prefix="/users/{source_user_id}/accounts/{source_account_type}/transactions", tags=["transactions"])
