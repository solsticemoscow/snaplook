from fastapi import APIRouter

from app.api.auth import router as auth_router
from app.api.users import router as users_router
from app.api.system import router as system_router
from app.api.payments import router as payments_router

router = APIRouter()

router.include_router(auth_router, prefix='/auth', tags=["Auth"])
router.include_router(system_router, prefix='/system', tags=["System"])
router.include_router(users_router, prefix='/users', tags=["Users"])
router.include_router(payments_router, prefix='/payments', tags=["Payments"])



