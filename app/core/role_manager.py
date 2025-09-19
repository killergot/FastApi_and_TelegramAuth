USER_ROLE: int = 0 # anyone
ADMIN_ROLE: int = 1   # 2^0

class RoleManager:
    @staticmethod
    def is_admin(user) -> bool:
        return user.role & ADMIN_ROLE