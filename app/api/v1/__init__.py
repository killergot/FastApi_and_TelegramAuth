from fastapi import APIRouter

from .auth import router as auth_router
from .users import router as users_router
from .sessions import router as sessions_router


router = APIRouter(prefix="/v1")
router.include_router(auth_router)
router.include_router(users_router)
router.include_router(sessions_router)