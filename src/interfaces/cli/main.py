import asyncio
import typer
from typing import Optional

from ...config import settings
from ...infrastructure.database.session import create_session_factory
from ...infrastructure.services.user_service_impl import UserServiceImpl
from ...infrastructure.database.repositories.user_repository_impl import UserRepositoryImpl
from ...application.use_cases.user_management import UserManagementUseCase
from .commands import users

app = typer.Typer(
    name="tg-bot-cli",
    help="CLI для управления Telegram ботом",
    add_completion=False,
)

# Добавляем подкоманды
app.add_typer(users.app, name="users", help="Управление пользователями")


@app.command()
def version() -> None:
    """Показать версию приложения."""
    typer.echo("Telegram Bot CLI v1.0.0")


async def get_user_management() -> UserManagementUseCase:
    """Получение экземпляра UserManagementUseCase."""
    session_factory = await create_session_factory()
    user_repository = UserRepositoryImpl(session_factory())
    user_service = UserServiceImpl(user_repository)
    return UserManagementUseCase(user_service)


def run_cli() -> None:
    """Запуск CLI приложения."""
    app()


if __name__ == "__main__":
    run_cli() 