from typing import AsyncGenerator, Optional

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.config import settings


async def create_session_factory() -> async_sessionmaker[AsyncSession]:
    """Создание фабрики сессий для работы с базой данных."""
    # Создание асинхронного движка
    engine = create_async_engine(
        f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@"
        f"{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}",
        echo=False,
    )

    # Создание фабрики сессий
    async_session = async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    return async_session


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Получение сессии для работы с базой данных."""
    async_session = await create_session_factory()
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close() 