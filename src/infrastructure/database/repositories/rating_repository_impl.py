from typing import List

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from ....domain.entities.user import User
from ....domain.repositories.rating_repository import RatingRepository
from ..models import UserModel


class RatingRepositoryImpl(RatingRepository):
    """Реализация репозитория для работы с рейтингом пользователей."""
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def increment_taps(self, user_id: int) -> User:
        """Увеличить количество нажатий пользователя."""
        # Получаем пользователя
        stmt = select(UserModel).where(UserModel.id == user_id)
        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()
        
        if user:
            # Увеличиваем количество нажатий
            user.taps += 1
            await self.session.commit()
            await self.session.refresh(user)
        
        return User.model_validate(user) if user else None
    
    async def get_top_users(self, limit: int = 10) -> List[User]:
        """Получить список пользователей с наивысшим рейтингом."""
        # Получаем пользователей, отсортированных по количеству нажатий
        stmt = (
            select(UserModel)
            .order_by(UserModel.taps.desc())
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        users = result.scalars().all()
        
        return [User.model_validate(user) for user in users]
    
    async def get_total_taps(self) -> int:
        """Получить общее количество нажатий всех пользователей."""
        # Получаем сумму нажатий всех пользователей
        stmt = select(func.sum(UserModel.taps))
        result = await self.session.execute(stmt)
        total = result.scalar_one_or_none()
        
        return total or 0
    
    async def update_user_info(self, user_id: int, info: str) -> User:
        """Обновить дополнительную информацию о пользователе."""
        # Получаем пользователя
        stmt = select(UserModel).where(UserModel.id == user_id)
        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()
        
        if user:
            # Обновляем информацию
            user.info = info
            await self.session.commit()
            await self.session.refresh(user)
        
        return User.model_validate(user) if user else None
    
    async def update_user_photo(self, user_id: int, photo_url: str) -> User:
        """Обновить фотографию пользователя."""
        # Получаем пользователя
        stmt = select(UserModel).where(UserModel.id == user_id)
        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()
        
        if user:
            # Обновляем фотографию
            user.photo = photo_url
            await self.session.commit()
            await self.session.refresh(user)
        
        return User.model_validate(user) if user else None 