from abc import ABC, abstractmethod
from typing import Optional, List

from ..entities.user import User


class UserRepository(ABC):
    """Интерфейс репозитория для работы с пользователями."""

    @abstractmethod
    async def get_by_id(self, user_id: int) -> Optional[User]:
        """Получить пользователя по ID."""
        pass

    @abstractmethod
    async def get_by_telegram_id(self, telegram_id: int) -> Optional[User]:
        """Получить пользователя по Telegram ID."""
        pass

    @abstractmethod
    async def create(self, user: User) -> User:
        """Создать нового пользователя."""
        pass

    @abstractmethod
    async def update(self, user: User) -> User:
        """Обновить существующего пользователя."""
        pass

    @abstractmethod
    async def delete(self, user_id: int) -> None:
        """Удалить пользователя."""
        pass

    @abstractmethod
    async def list_all(self) -> List[User]:
        """Получить список всех пользователей."""
        pass

    @abstractmethod
    async def list_active(self) -> List[User]:
        """Получить список активных пользователей."""
        pass 