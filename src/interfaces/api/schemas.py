from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class UserBase(BaseModel):
    """Базовая схема пользователя."""
    telegram_id: int = Field(..., description="Telegram ID пользователя")
    username: Optional[str] = Field(None, description="Имя пользователя в Telegram")
    first_name: Optional[str] = Field(None, description="Имя пользователя")
    last_name: Optional[str] = Field(None, description="Фамилия пользователя")
    is_active: bool = Field(True, description="Активен ли пользователь")
    is_admin: bool = Field(False, description="Является ли пользователь администратором")


class UserCreate(UserBase):
    """Схема для создания пользователя."""
    pass


class UserUpdate(UserBase):
    """Схема для обновления пользователя."""
    telegram_id: Optional[int] = Field(None, description="Telegram ID пользователя")
    is_active: Optional[bool] = Field(None, description="Активен ли пользователь")
    is_admin: Optional[bool] = Field(None, description="Является ли пользователь администратором")


class UserInDB(UserBase):
    """Схема пользователя в базе данных."""
    id: int = Field(..., description="ID пользователя")
    created_at: datetime = Field(..., description="Дата создания")
    updated_at: datetime = Field(..., description="Дата обновления")

    class Config:
        from_attributes = True


class UserResponse(UserInDB):
    """Схема ответа с данными пользователя."""
    pass 