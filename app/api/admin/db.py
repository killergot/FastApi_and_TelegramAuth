from fastapi import APIRouter

from app.database import create_db

router = APIRouter(prefix="/db")

@router.post("/refresh")
async def refresh():
    await create_db()
    return {'ok': True}
