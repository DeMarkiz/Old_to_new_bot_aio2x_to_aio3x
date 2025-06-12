from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Настройки приложения."""
    
    # Telegram
    BOT_TOKEN: str
    ADMIN_IDS: list[int] = []
    CREATOR_ID: int
    
    # Database
    DATABASE_URL: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    
    # API
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_PREFIX: str = "/api/v1"
    
    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: str | None = None
    
    # FSM Redis
    FSM_REDIS_HOST: str
    FSM_REDIS_DB: int
    FSM_REDIS_PASS: str | None = None
    
    # Bot settings
    REGISTER_PASSPHRASE: str
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="allow"  # Разрешаем дополнительные поля
    )


settings = Settings() 