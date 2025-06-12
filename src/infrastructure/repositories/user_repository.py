from typing import Optional, List
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities.user import User
from src.domain.repositories.user_repository import UserRepository


class UserRepositoryImpl(UserRepository):
    """Реализация репозитория для работы с пользователями."""

    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_by_id(self, user_id: int) -> Optional[User]:
        """Получить пользователя по ID."""
        result = await self._session.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_by_telegram_id(self, telegram_id: int) -> Optional[User]:
        """Получить пользователя по Telegram ID."""
        result = await self._session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        return result.scalar_one_or_none()

    async def create(self, user: User) -> User:
        """Создать нового пользователя."""
        self._session.add(user)
        await self._session.commit()
        await self._session.refresh(user)
        return user

    async def update(self, user: User) -> User:
        """Обновить существующего пользователя."""
        await self._session.merge(user)
        await self._session.commit()
        return user

    async def delete(self, user_id: int) -> None:
        """Удалить пользователя."""
        await self._session.execute(
            delete(User).where(User.id == user_id)
        )
        await self._session.commit()

    async def list_all(self) -> List[User]:
        """Получить список всех пользователей."""
        result = await self._session.execute(select(User))
        return list(result.scalars().all())

    async def list_active(self) -> List[User]:
        """Получить список активных пользователей."""
        result = await self._session.execute(
            select(User).where(User.is_active == True)
        )
        return list(result.scalars().all()) 