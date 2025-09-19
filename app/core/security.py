from app.core.config import load_config
from app.utils.jwt import encode_jwt, decode_jwt
from datetime import datetime, timedelta



config = load_config()

SECRET_KEY = config.secret_keys.jwt
REFRESH_SECRET_KEY = config.secret_keys.jwt_refresh
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_SECONDS = 60 * 60 * 24 * 30 # Потом поменять на 15 минут
REFRESH_TOKEN_EXPIRE_SECONDS = 60 * 60 * 24 * 30  # 30 дней


def create_access_token(user_id: int,
                        user_telegram_id: int,
                        user_role: int) -> str:
    expire = datetime.utcnow() + timedelta(seconds=ACCESS_TOKEN_EXPIRE_SECONDS)
    payload = {
        'id': user_id,
        'telegram_id': user_telegram_id,
        'role': user_role,
        'exp': expire
    }
    return encode_jwt(payload, SECRET_KEY, ALGORITHM)

def create_refresh_token(user_id: int) -> str:
    expire = datetime.utcnow() + timedelta(seconds=REFRESH_TOKEN_EXPIRE_SECONDS)
    payload = {
        'sub': str(user_id),
        'exp': expire
    }
    return encode_jwt(payload, REFRESH_SECRET_KEY, ALGORITHM)

def decode_access_token(token: str) -> dict:
    return decode_jwt(token, secret=SECRET_KEY)

def decode_refresh_token(token: str) -> dict:
    return decode_jwt(token, secret=REFRESH_SECRET_KEY)




if __name__ == '__main__':
    a = create_access_token(1,'test',1)
    print(a)
    print(decode_access_token(a))




