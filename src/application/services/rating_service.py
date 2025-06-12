from abc import ABC, abstractmethod
from typing import List

from ...domain.entities.user import User
from ...domain.repositories.rating_repository import RatingRepository


class RatingService(ABC):
    """Интерфейс сервиса для работы с рейтингом пользователей."""
    
    def __init__(self, rating_repository: RatingRepository):
        self.rating_repository = rating_repository
    
    @abstractmethod
    async def increment_taps(self, user_id: int) -> User:
        """Увеличить количество нажатий пользователя."""
        pass
    
    @abstractmethod
    async def get_top_users(self, limit: int = 10) -> List[User]:
        """Получить список пользователей с наивысшим рейтингом."""
        pass
    
    @abstractmethod
    async def get_total_taps(self) -> int:
        """Получить общее количество нажатий всех пользователей."""
        pass
    
    @abstractmethod
    async def update_user_info(self, user_id: int, info: str) -> User:
        """Обновить дополнительную информацию о пользователе."""
        pass
    
    @abstractmethod
    async def update_user_photo(self, user_id: int, photo_url: str) -> User:
        """Обновить фотографию пользователя."""
        pass 