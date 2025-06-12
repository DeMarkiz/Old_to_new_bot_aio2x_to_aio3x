FROM python:3.11-slim

WORKDIR /app

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Копирование файлов зависимостей
COPY requirements.txt .
COPY pyproject.toml .
COPY README.md .

# Установка зависимостей Python
RUN pip install --no-cache-dir -r requirements.txt

# Добавляем директорию проекта в PYTHONPATH
ENV PYTHONPATH=/app

# Применение миграций при запуске
CMD sh -c "alembic upgrade head && python -m src.interfaces.bot.main"
