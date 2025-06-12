from abc import ABC, abstractmethod
from typing import Optional

from src.domain.entities.user import User


class UserService(ABC):
    """Интерфейс сервиса пользователей"""
    
    @abstractmethod
    async def get_user(self, telegram_id: int) -> Optional[User]:
        """Получение пользователя по Telegram ID"""
        pass
    
    @abstractmethod
    async def create_user(self, telegram_id: int, name: str, info: str = "", photo: str = "") -> User:
        """Создание нового пользователя"""
        pass
    
    @abstractmethod
    async def update_user(self, telegram_id: int, name: str = None, info: str = None, photo: str = None) -> User:
        """Обновление данных пользователя"""
        pass
    
    @abstractmethod
    async def deactivate_user(self, telegram_id: int) -> None:
        """Деактивация пользователя"""
        pass 