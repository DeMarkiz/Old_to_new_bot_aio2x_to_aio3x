from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import settings
from .dependencies import get_user_management
from .routers import users


def create_app() -> FastAPI:
    """Создание экземпляра FastAPI приложения."""
    app = FastAPI(
        title="Telegram Bot API",
        description="API для управления Telegram ботом",
        version="1.0.0",
        docs_url=f"{settings.API_PREFIX}/docs",
        redoc_url=f"{settings.API_PREFIX}/redoc",
        openapi_url=f"{settings.API_PREFIX}/openapi.json",
    )

    # Настройка CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Подключение роутеров
    app.include_router(
        users.router,
        prefix=f"{settings.API_PREFIX}/users",
        tags=["users"],
    )

    return app


app = create_app() 