from fastapi import APIRouter
from . import accounts, users
from . import auth

router = APIRouter()
router.include_router(accounts.router, prefix="/accounts", tags=["accounts"])
router.include_router(users.router, prefix="/users", tags=["users"])
router.include_router(auth.router, prefix="/auth", tags=["auth"])