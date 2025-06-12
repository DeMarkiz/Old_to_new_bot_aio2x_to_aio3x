import asyncio
from typing import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from src.domain.entities.user import User
from src.infrastructure.database.models import Base
from src.infrastructure.database.repositories.user_repository_impl import UserRepositoryImpl
from src.infrastructure.services.user_service_impl import UserServiceImpl
from src.application.use_cases.user_management import UserManagementUseCase


# Тестовые данные
TEST_USER = User(
    id=1,
    telegram_id=123456789,
    username="test_user",
    first_name="Test",
    last_name="User",
    created_at=None,  # Будет установлено при создании
    updated_at=None,  # Будет установлено при создании
    is_active=True,
    is_admin=False,
)


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Создание event loop для тестов."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def test_engine():
    """Создание тестового движка базы данных."""
    # Используем in-memory SQLite для тестов
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        echo=False,
        poolclass=NullPool,
    )
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield engine
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    
    await engine.dispose()


@pytest_asyncio.fixture
async def test_session(test_engine) -> AsyncGenerator[AsyncSession, None]:
    """Создание тестовой сессии."""
    async_session = sessionmaker(
        test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    
    async with async_session() as session:
        yield session
        await session.rollback()


@pytest_asyncio.fixture
async def user_repository(test_session) -> UserRepositoryImpl:
    """Создание репозитория пользователей."""
    return UserRepositoryImpl(test_session)


@pytest_asyncio.fixture
async def user_service(user_repository) -> UserServiceImpl:
    """Создание сервиса пользователей."""
    return UserServiceImpl(user_repository)


@pytest_asyncio.fixture
async def user_management(user_service) -> UserManagementUseCase:
    """Создание use case для управления пользователями."""
    return UserManagementUseCase(user_service)


@pytest_asyncio.fixture
async def test_user(user_management) -> User:
    """Создание тестового пользователя."""
    return await user_management.create_user(
        telegram_id=TEST_USER.telegram_id,
        username=TEST_USER.username,
        first_name=TEST_USER.first_name,
        last_name=TEST_USER.last_name,
    ) 