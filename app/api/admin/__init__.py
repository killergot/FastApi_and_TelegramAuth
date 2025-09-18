from fastapi import APIRouter

from .db import router as db_router

router = APIRouter(prefix="/admin", tags=["admin"])

router.include_router(db_router)