from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete

from src.application.services.user_service import UserService
from src.domain.entities.user import User
from src.infrastructure.repositories.user_repository import UserRepositoryImpl


class UserServiceImpl(UserService):
    """Реализация сервиса пользователей"""

    def __init__(self, repository: UserRepositoryImpl):
        self.repository = repository
    
    async def get_user(self, telegram_id: int) -> Optional[User]:
        """Получить пользователя по telegram_id"""
        return await self.repository.get_by_telegram_id(telegram_id)
    
    async def create_user(self, telegram_id: int, name: str, info: str, photo: str) -> User:
        """Создать нового пользователя"""
        user = User(
            telegram_id=telegram_id,
            name=name,
            info=info,
            photo=photo
        )
        return await self.repository.create(user)
    
    async def update_user(self, telegram_id: int, name: str, info: str, photo: str) -> Optional[User]:
        """Обновить данные пользователя"""
        user = await self.get_user(telegram_id)
        if not user:
            return None
            
        user.name = name
        user.info = info
        user.photo = photo
        return await self.repository.update(user)
    
    async def deactivate_user(self, telegram_id: int) -> bool:
        """Деактивировать пользователя"""
        user = await self.get_user(telegram_id)
        if not user:
            return False
            
        user.is_active = False
        await self.repository.update(user)
        return True

    async def get_by_id(self, user_id: int) -> Optional[User]:
        """Получить пользователя по ID."""
        return await self.repository.get_by_id(user_id)

    async def update(self, user: User) -> User:
        """Обновить существующего пользователя."""
        return await self.repository.update(user)

    async def delete(self, user_id: int) -> None:
        """Удалить пользователя."""
        await self.repository.delete(user_id)

    async def list_all(self) -> List[User]:
        """Получить список всех пользователей."""
        return await self.repository.list_all()

    async def list_active(self) -> List[User]:
        """Получить список активных пользователей."""
        return await self.repository.list_active() 