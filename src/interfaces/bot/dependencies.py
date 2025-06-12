from typing import Annotated
from aiogram import Dispatcher
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import BaseStorage
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from src.infrastructure.services.user_service_impl import UserServiceImpl
from src.infrastructure.services.rating_service_impl import RatingServiceImpl
from src.infrastructure.database.repositories.user_repository_impl import UserRepositoryImpl
from src.infrastructure.database.repositories.rating_repository_impl import RatingRepositoryImpl

# Глобальные экземпляры сервисов
_user_service = None
_rating_service = None

def setup_dependencies(dp: Dispatcher, session_factory: async_sessionmaker[AsyncSession]) -> None:
    """Настройка зависимостей для бота"""
    global _user_service, _rating_service
    
    # Инициализация репозиториев
    user_repository = UserRepositoryImpl(session_factory)
    rating_repository = RatingRepositoryImpl(session_factory)
    
    # Инициализация сервисов
    _user_service = UserServiceImpl(user_repository)
    _rating_service = RatingServiceImpl(rating_repository)
    
    # Регистрация middleware
    dp.update.middleware.register(DependencyMiddleware())

def get_user_service() -> UserServiceImpl:
    """Получение сервиса пользователей"""
    if _user_service is None:
        raise RuntimeError("User service not initialized")
    return _user_service

def get_rating_service() -> RatingServiceImpl:
    """Получение сервиса рейтинга"""
    if _rating_service is None:
        raise RuntimeError("Rating service not initialized")
    return _rating_service

class DependencyMiddleware:
    """Middleware для внедрения зависимостей"""
    
    async def __call__(
        self,
        handler,
        event,
        data: dict
    ):
        # Добавление сервисов в данные
        data["user_service"] = get_user_service()
        data["rating_service"] = get_rating_service()
        
        return await handler(event, data) 