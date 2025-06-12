import logging
import asyncio
from datetime import datetime, timedelta

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from loguru import logger

from src.application.use_cases.user_management import UserManagementUseCase
from src.application.use_cases.rating_management import RatingManagementUseCase
from src.config import settings
from src.infrastructure.database.session import create_session_factory
from src.infrastructure.services.user_service_impl import UserServiceImpl
from src.infrastructure.database.repositories.user_repository_impl import UserRepositoryImpl


logger = logging.getLogger(__name__)


async def send_daily_digest(
    bot,
    user_management: UserManagementUseCase,
    rating_management: RatingManagementUseCase,
) -> None:
    """Отправка ежедневного дайджеста пользователям."""
    try:
        # Получаем всех активных пользователей
        users = await user_management.get_users(active=True)
        
        # Получаем топ пользователей
        top_users = await rating_management.get_top_users(limit=5)
        
        # Получаем общее количество нажатий
        total_taps = await rating_management.get_total_taps()
        
        # Формируем сообщение
        text = (
            "📊 Ежедневный дайджест\n\n"
            f"Всего нажатий: {total_taps}\n\n"
            "Топ пользователей:\n"
        )
        
        for i, user in enumerate(top_users, 1):
            text += f"{i}. {user.username or 'Аноним'}: {user.taps}\n"
        
        # Отправляем сообщение всем пользователям
        for user in users:
            try:
                await bot.send_message(user.telegram_id, text)
            except Exception as e:
                logger.error(f"Failed to send digest to user {user.telegram_id}: {e}")
    
    except Exception as e:
        logger.error(f"Failed to send daily digest: {e}")


async def setup_scheduler(
    bot,
    user_management: UserManagementUseCase,
    rating_management: RatingManagementUseCase,
) -> AsyncIOScheduler:
    """Настройка и запуск планировщика задач."""
    scheduler = AsyncIOScheduler()
    
    # Добавляем задачу отправки ежедневного дайджеста
    scheduler.add_job(
        send_daily_digest,
        CronTrigger(hour=20, minute=0),  # Каждый день в 20:00
        args=[bot, user_management, rating_management],
        id="daily_digest",
        replace_existing=True,
    )
    
    # Запускаем планировщик
    scheduler.start()
    logger.info("Scheduler started")
    
    return scheduler 