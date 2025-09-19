from pydantic import BaseModel



class UserLoginTelegram(BaseModel):
    telegram_id: int
    last_name: str
    first_name: str
    photo_url: str
    username: str

class UserLoginTelegramIn(UserLoginTelegram):
    auth_date: str
    hash: str

    class Config:
        allow_population_by_field_name = True
        extra = "ignore"  # игнорировать лишние поля



class TokenOut(BaseModel):
    access_token: str
    refresh_token: str
    type:str = 'Bearer'

    model_config = {
        'from_attributes': True
    }
