from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class User(BaseModel):
    """Сущность пользователя."""
    
    id: Optional[int] = None
    telegram_id: int
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    is_active: bool = True
    is_admin: bool = False
    
    # Дополнительные поля для рейтинга
    taps: int = Field(default=0, description="Количество нажатий")
    info: Optional[str] = Field(default=None, description="Дополнительная информация о пользователе")
    photo: Optional[str] = Field(default=None, description="URL фотографии пользователя")
    
    class Config:
        from_attributes = True 