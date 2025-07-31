from fastapi import APIRouter

from app.api.endpoints import login, users, transactions

api_router = APIRouter(redirect_slashes=False)
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(transactions.router, prefix="/transactions", tags=["transactions", "metrics"])

# In the future, we will include routers from other files here
# from .endpoints import login, transactions
# api_router.include_router(login.router, tags=["login"])
# api_router.include_router(transactions.router, prefix="/transactions", tags=["transactions"]) 