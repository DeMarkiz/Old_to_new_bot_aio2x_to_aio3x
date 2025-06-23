from typing import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.use_cases.user_management import UserManagementUseCase
from src.infrastructure.database.session import get_session
from src.infrastructure.services.user_service_impl import UserServiceImpl
from src.infrastructure.services.rating_service_impl import RatingServiceImpl
from src.infrastructure.database.repositories.user_repository_impl import UserRepositoryImpl
from src.infrastructure.database.repositories.rating_repository_impl import RatingRepositoryImpl


async def get_user_management(
    session: AsyncSession = Depends(get_session),
) -> AsyncGenerator[UserManagementUseCase, None]:
    """Получение экземпляра UserManagementUseCase."""
    user_repository = UserRepositoryImpl(session)
    user_service = UserServiceImpl(user_repository)
    user_management = UserManagementUseCase(user_service)
    
    try:
        yield user_management
    finally:
        await session.close()


async def get_user_service(
    session: AsyncSession = Depends(get_session),
) -> AsyncGenerator[UserServiceImpl, None]:
    """Получение сервиса пользователей"""
    user_repository = UserRepositoryImpl(session)
    user_service = UserServiceImpl(user_repository)
    
    try:
        yield user_service
    finally:
        await session.close()


async def get_rating_service(
    session: AsyncSession = Depends(get_session),
) -> AsyncGenerator[RatingServiceImpl, None]:
    """Получение сервиса рейтинга"""
    rating_repository = RatingRepositoryImpl(session)
    rating_service = RatingServiceImpl(rating_repository)
    
    try:
        yield rating_service
    finally:
        await session.close() 