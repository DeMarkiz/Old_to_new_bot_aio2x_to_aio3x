from datetime import datetime
from typing import Optional, List

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from ....domain.entities.user import User
from ....domain.repositories.user_repository import UserRepository
from ..models import UserModel


class UserRepositoryImpl(UserRepository):
    """Реализация репозитория для работы с пользователями через SQLAlchemy."""

    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_by_id(self, user_id: int) -> Optional[User]:
        """Получить пользователя по ID."""
        query = select(UserModel).where(UserModel.id == user_id)
        async with self._session() as session:
            result = await session.execute(query)
        user_model = result.scalar_one_or_none()
        
        if user_model is None:
            return None
            
        return self._to_domain(user_model)

    async def get_by_telegram_id(self, telegram_id: int) -> Optional[User]:
        """Получить пользователя по Telegram ID."""
        query = select(UserModel).where(UserModel.telegram_id == telegram_id)
        async with self._session() as session:
            result = await session.execute(query)
        user_model = result.scalar_one_or_none()
        
        if user_model is None:
            return None
            
        return self._to_domain(user_model)

    async def create(self, user: User) -> User:
        """Создать нового пользователя."""
        user_model = UserModel(
            telegram_id=user.telegram_id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            created_at=user.created_at,
            updated_at=user.updated_at,
            is_active=user.is_active,
            is_admin=user.is_admin,
        )
        
        async with self._session() as session:
            session.add(user_model)
            await session.flush()
        
        return self._to_domain(user_model)

    async def update(self, user: User) -> User:
        """Обновить существующего пользователя."""
        query = (
            update(UserModel)
            .where(UserModel.id == user.id)
            .values(
                telegram_id=user.telegram_id,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name,
                updated_at=user.updated_at,
                is_active=user.is_active,
                is_admin=user.is_admin,
            )
        )
        
        async with self._session() as session:
            await session.execute(query)
        return user

    async def delete(self, user_id: int) -> None:
        """Удалить пользователя."""
        query = delete(UserModel).where(UserModel.id == user_id)
        async with self._session() as session:
            await session.execute(query)

    async def list_all(self) -> List[User]:
        """Получить список всех пользователей."""
        query = select(UserModel)
        async with self._session() as session:
            result = await session.execute(query)
        user_models = result.scalars().all()
        
        return [self._to_domain(model) for model in user_models]

    async def list_active(self) -> List[User]:
        """Получить список активных пользователей."""
        query = select(UserModel).where(UserModel.is_active == True)
        async with self._session() as session:
            result = await session.execute(query)
        user_models = result.scalars().all()
        
        return [self._to_domain(model) for model in user_models]

    def _to_domain(self, model: UserModel) -> User:
        """Преобразовать модель в доменную сущность."""
        return User(
            id=model.id,
            telegram_id=model.telegram_id,
            username=model.username,
            first_name=model.first_name,
            last_name=model.last_name,
            created_at=model.created_at,
            updated_at=model.updated_at,
            is_active=model.is_active,
            is_admin=model.is_admin,
        ) 