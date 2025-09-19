from app.database.models.auth import User
from app.shemas.users import UserOut

USER_ROLE: int = 0 # anyone
ADMIN_ROLE: int = 1   # 2^0

class RoleManager:
    @staticmethod
    def is_admin(user: UserOut| User) -> bool:
        return bool(user.role & ADMIN_ROLE)