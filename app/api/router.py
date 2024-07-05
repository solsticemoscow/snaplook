from fastapi import APIRouter

from app.api.auth import router as auth_router
from app.api.system import router as system_router


router = APIRouter(prefix="/api")

router.include_router(auth_router, prefix='/auth')
router.include_router(system_router, prefix='/system')


