from uuid import UUID

from fastapi import Depends, status
from fastapi.routing import APIRouter


from app.api.depencies.guard import get_current_user
from app.api.depencies.services import get_user_service
from app.services.user import UserService
from app.shemas.users import UserOut

router = APIRouter(prefix="/sessions", tags=["users"])

@router.get("/my", status_code=status.HTTP_200_OK)
async def get_all_users(user_service: UserService = Depends(get_user_service),
                        user: UserOut = Depends(get_current_user)):
    return await user_service.get_sessions(user.id)

@router.delete("/my/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_session(session_id: UUID,
                         user: UserOut = Depends(get_current_user),
                         user_service: UserService = Depends(get_user_service)):
    return await user_service.delete_session(session_id, user.id)