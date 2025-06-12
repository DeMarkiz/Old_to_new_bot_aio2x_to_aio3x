from datetime import datetime
from typing import Optional, List

from ..interfaces.user_service import UserService
from ...domain.entities.user import User


class UserManagementUseCase:
    """Use case для управления пользователями."""

    def __init__(self, user_service: UserService):
        self._user_service = user_service

    async def get_user(self, user_id: int) -> Optional[User]:
        """Получить пользователя по ID."""
        return await self._user_service.get_by_id(user_id)

    async def get_user_by_telegram_id(self, telegram_id: int) -> Optional[User]:
        """Получить пользователя по Telegram ID."""
        return await self._user_service.get_by_telegram_id(telegram_id)

    async def create_user(
        self,
        telegram_id: int,
        username: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
    ) -> User:
        """Создать нового пользователя."""
        now = datetime.utcnow()
        user = User(
            id=0,  # ID будет установлен при сохранении
            telegram_id=telegram_id,
            username=username,
            first_name=first_name,
            last_name=last_name,
            created_at=now,
            updated_at=now,
        )
        return await self._user_service.create(user)

    async def update_user(self, user: User) -> User:
        """Обновить существующего пользователя."""
        user.updated_at = datetime.utcnow()
        return await self._user_service.update(user)

    async def delete_user(self, user_id: int) -> None:
        """Удалить пользователя."""
        await self._user_service.delete(user_id)

    async def list_all_users(self) -> List[User]:
        """Получить список всех пользователей."""
        return await self._user_service.list_all()

    async def list_active_users(self) -> List[User]:
        """Получить список активных пользователей."""
        return await self._user_service.list_active() 