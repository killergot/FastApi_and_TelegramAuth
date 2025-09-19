from pydantic import BaseModel, EmailStr, field_validator, Field
from typing import Optional, Literal
from datetime import datetime
from uuid import UUID

MIN_LEN_PASS: int = 2

MIN_LEN_PASS: int = 2

class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    role: Optional[int] = Field(ge=0, le=7)
    auth_provider: Optional[Literal['google', 'facebook', 'github','yandex']] = None
    provider_id: Optional[str] = None

    @field_validator('provider_id')
    @classmethod
    def check_provider(cls, v, values):
        if values.data.get('auth_provider') and not v:
            raise ValueError('provider_id required for OAuth')
        if v and not values.data.get('auth_provider'):
            raise ValueError('auth_provider required when provider_id is set')
        return v


class UserUpdateIn(BaseModel):
    telegram_id: Optional[int] = None
    last_name: Optional[str] = None
    first_name: Optional[str] = None
    photo_url: Optional[str] = None
    username: Optional[str] = None
    email: Optional[str] = None


class UserTelegramInfo(BaseModel):
    telegram_id: int
    last_name: str
    first_name: str
    photo_url: str
    username: str


class UserOut(UserBase,UserTelegramInfo):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    model_config = {
        'from_attributes': True
    }

