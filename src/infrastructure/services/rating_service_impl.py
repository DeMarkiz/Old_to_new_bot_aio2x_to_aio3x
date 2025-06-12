from typing import List

from ...application.services.rating_service import RatingService
from ...domain.entities.user import User
from ...domain.repositories.rating_repository import RatingRepository


class RatingServiceImpl(RatingService):
    """Реализация сервиса для работы с рейтингом пользователей."""
    
    def __init__(self, rating_repository: RatingRepository):
        super().__init__(rating_repository)
    
    async def increment_taps(self, user_id: int) -> User:
        """Увеличить количество нажатий пользователя."""
        return await self.rating_repository.increment_taps(user_id)
    
    async def get_top_users(self, limit: int = 10) -> List[User]:
        """Получить список пользователей с наивысшим рейтингом."""
        return await self.rating_repository.get_top_users(limit)
    
    async def get_total_taps(self) -> int:
        """Получить общее количество нажатий всех пользователей."""
        return await self.rating_repository.get_total_taps()
    
    async def update_user_info(self, user_id: int, info: str) -> User:
        """Обновить дополнительную информацию о пользователе."""
        return await self.rating_repository.update_user_info(user_id, info)
    
    async def update_user_photo(self, user_id: int, photo_url: str) -> User:
        """Обновить фотографию пользователя."""
        return await self.rating_repository.update_user_photo(user_id, photo_url) 