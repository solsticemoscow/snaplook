from fastapi import APIRouter

from app.api.auth import router as auth_router
from app.api.users import router as users_router
from app.api.system import router as system_router


router = APIRouter()

router.include_router(users_router, prefix='/users')
router.include_router(auth_router, prefix='/auth')
router.include_router(system_router, prefix='/system')


