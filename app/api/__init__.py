from fastapi import APIRouter

from .v1 import router as v1_router
from .admin import router as admin_router

router = APIRouter()
router.include_router(v1_router)
router.include_router(admin_router)
