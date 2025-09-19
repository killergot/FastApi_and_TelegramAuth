from fastapi import Depends, status
from fastapi.routing import APIRouter


from app.api.depencies.guard import get_current_user, require_role
from app.api.depencies.services import get_user_service
from app.core.role_manager import ADMIN_ROLE

router = APIRouter(prefix="/sessions", tags=["users"])

@router.get("/my", status_code=status.HTTP_200_OK)
async def get_all_users(user_service = Depends(get_user_service),
                        user = Depends(get_current_user)):
    return await user_service.get_sessions(user.id)

@router.delete("/my/{session_id}", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(get_current_user)])
async def delete_session(session_id: str, user_service = Depends(get_user_service)):
    return await user_service.delete_session(session_id)