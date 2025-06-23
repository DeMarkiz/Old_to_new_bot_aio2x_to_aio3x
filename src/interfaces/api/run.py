import uvicorn

from src.config import settings
from .main import app


def run_api() -> None:
    """Запуск FastAPI приложения."""
    uvicorn.run(
        "src.interfaces.api.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=True,
    )


if __name__ == "__main__":
    run_api() 