from aiogram import Dispatcher, types
from aiogram.types import Message
from aiogram.exceptions import TelegramBadRequest, TelegramRetryAfter, TelegramAPIError
from loguru import logger

from src.interfaces.bot.dependencies import get_user_service


class Errors:
    """Сообщения об ошибках."""
    
    please_register = "Пожалуйста, зарегистрируйтесь для использования бота."
    register_failed = "Регистрация не удалась. Убедитесь, что у вас установлено имя пользователя."
    text = "What? Dont understand."
    text_form = "Не вижу в сообщении текста, попробуйте еще раз!"
    bot_blocked = "Бот заблокирован пользователем"
    retry_after = "Слишком много запросов, попробуйте позже"
    api_error = "Ошибка API Telegram"

    @staticmethod
    async def register_error_handlers(dp: Dispatcher) -> None:
        """Регистрация обработчиков ошибок"""
        dp.errors.register(Errors.handle_telegram_errors)

    @staticmethod
    async def handle_telegram_errors(event: types.Update, exception: Exception, data: dict) -> None:
        """Обработка ошибок Telegram API"""
        if isinstance(exception, TelegramBadRequest):
            if hasattr(event, 'from_user') and "bot was blocked by the user" in str(exception).lower():
                user_service = get_user_service()
                await user_service.deactivate_user(event.from_user.id)
                logger.warning(f"User {event.from_user.id} blocked the bot")
            else:
                logger.error(f"Telegram API error: {exception}")

        elif isinstance(exception, TelegramRetryAfter):
            logger.warning(f"Rate limit exceeded. Retry after {exception.retry_after} seconds")

        elif isinstance(exception, TelegramAPIError):
            logger.error(f"Telegram API error: {exception}")

        else:
            logger.exception(f"Unexpected error: {exception}")


async def handle_bot_blocked(update: Message, exception: TelegramBadRequest) -> bool:
    """Обработка ошибки блокировки бота пользователем."""
    logger.info(f"User {update.from_user.id} blocked the bot")
    logger.info(exception)
    return True


async def handle_retry_after(update: Message, exception: TelegramRetryAfter) -> bool:
    """Обработка ошибки превышения лимита запросов."""
    logger.warning(f"Rate limit exceeded. Retry after {exception.retry_after} seconds")
    return True


def register_error_handlers(dp: Dispatcher) -> None:
    """Регистрация обработчиков ошибок."""
    dp.errors.register(handle_bot_blocked, exception=TelegramBadRequest)
    dp.errors.register(handle_retry_after, exception=TelegramRetryAfter) 