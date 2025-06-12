from typing import Any, Dict, Optional

from aiogram.filters import BaseFilter
from aiogram.types import Message

from src.config import settings
from src.application.use_cases.user_management import UserManagementUseCase
from src.interfaces.bot.dependencies import get_user_service


class CreatorFilter(BaseFilter):
    """Фильтр для проверки, является ли пользователь создателем бота."""
    
    async def __call__(self, message: Message) -> bool:
        """Проверка, является ли пользователь создателем бота."""
        return message.from_user.id in settings.ADMIN_IDS


class RegistrationFilter(BaseFilter):
    """Фильтр для проверки, зарегистрирован ли пользователь."""
    
    def __init__(self, user_management: UserManagementUseCase):
        self.user_management = user_management
    
    async def __call__(self, message: Message) -> bool:
        """Проверка, зарегистрирован ли пользователь."""
        user = await self.user_management.get_user_by_telegram_id(message.from_user.id)
        return user is not None


class NonRegistrationFilter(BaseFilter):
    """Фильтр для проверки, не зарегистрирован ли пользователь."""
    
    def __init__(self, user_management: UserManagementUseCase):
        self.user_management = user_management
    
    async def __call__(self, message: Message) -> bool:
        """Проверка, не зарегистрирован ли пользователь."""
        user = await self.user_management.get_user_by_telegram_id(message.from_user.id)
        return user is None


class UserFilter(BaseFilter):
    """Фильтр для проверки регистрации пользователя"""
    
    async def __call__(self, message: Message) -> bool:
        user_service = get_user_service()
        user = await user_service.get_user(message.from_user.id)
        return user is not None


class NonRegisteredUserFilter(BaseFilter):
    """Фильтр для проверки отсутствия регистрации пользователя"""
    
    async def __call__(self, message: Message) -> bool:
        user_service = get_user_service()
        user = await user_service.get_user(message.from_user.id)
        return user is None 