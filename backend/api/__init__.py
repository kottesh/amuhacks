from fastapi import APIRouter

from api.v1.endpoints import auth, users, accounts, transactions

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(accounts.router, prefix="/accounts", tags=["Accounts"])
api_router.include_router(transactions.router, prefix="/transactions", tags=["Transactions"])
