import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from loguru import logger

from src.config import settings
from src.infrastructure.database.session import create_session_factory
from src.interfaces.bot.handlers import register_handlers
from src.interfaces.bot.errors import Errors
from src.interfaces.bot.dependencies import setup_dependencies

async def main() -> None:
    """Основная функция запуска бота"""
    # Инициализация бота и диспетчера
    bot = Bot(token=settings.BOT_TOKEN)
    
    # Формирование URL для Redis
    redis_url = f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}"
    if settings.REDIS_PASSWORD:
        redis_url = f"redis://:{settings.REDIS_PASSWORD}@{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}"
    
    storage = RedisStorage.from_url(redis_url)
    dp = Dispatcher(storage=storage)
    
    # Настройка зависимостей
    session_factory = await create_session_factory()
    setup_dependencies(dp, session_factory)
    
    # Регистрация обработчиков
    register_handlers(dp)
    await Errors.register_error_handlers(dp)
    
    # Запуск бота
    logger.info("Starting bot...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main()) 