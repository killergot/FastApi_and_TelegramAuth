from fastapi import Depends, status
from fastapi.routing import APIRouter


from app.api.depencies.guard import get_current_user, require_role
from app.api.depencies.services import get_user_service
from app.core.role_manager import ADMIN_ROLE
from app.services.user import UserService
from app.shemas.users import UserOut, UserUpdateIn

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/get_me", response_model=UserOut, status_code=status.HTTP_200_OK)
async def get_me(user = Depends(get_current_user)):
    return user

@router.get("/get_user", response_model=UserOut, status_code=status.HTTP_200_OK,
            dependencies=[Depends(get_current_user)])
async def get_user_by_id(user_id: int,
                         user_service = Depends(get_user_service)):
    return await user_service.get_by_id(user_id)

@router.get("/get_all", status_code=status.HTTP_200_OK,
            dependencies=[Depends(require_role(ADMIN_ROLE))])
async def get_all_users(user_service: UserService = Depends(get_user_service)):
    return await user_service.get_all()

@router.put("/me", response_model=UserOut, status_code=status.HTTP_200_OK)
async def update_user(new_user: UserUpdateIn,
                      user: UserOut = Depends(get_current_user),
                      user_service: UserService = Depends(get_user_service)):
    return await user_service.update(user, new_user)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(require_role(ADMIN_ROLE))])
async def delete_user(user_id: int,
                      user_service: UserService = Depends(get_user_service)):
    await user_service.del_by_id(user_id)