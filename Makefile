# === Makefile для Old_to_new_bot_aio2x_to_aio3x ===

# Имя папки проекта
SERVICE_DIR := src

# Цвета для вывода
TXT_BOLD := \033[1m
TXT_MAGENTA := \033[35m
TXT_RESET := \033[0m

# Установка зависимостей poetry без установки самого проекта
setup:
	poetry install --no-root

# Установка pre-commit хуков
setup-pre-commit:
	poetry run pre-commit install

# Линтинг всего проекта: black, mypy, ruff
lint:
	@printf "${TXT_BOLD}${TXT_MAGENTA}========== BLACK ==========${TXT_RESET}\n"
	@poetry run black $(SERVICE_DIR)/
	@printf "${TXT_BOLD}${TXT_MAGENTA}=========== MYPY ==========${TXT_RESET}\n"
	@poetry run mypy $(SERVICE_DIR)/
	@printf "${TXT_BOLD}${TXT_MAGENTA}=========== RUFF ==========${TXT_RESET}\n"
	@poetry run ruff check --fix --show-fixes --exit-non-zero-on-fix .
	@printf "${TXT_BOLD}${TXT_MAGENTA}========= LINT DONE =======${TXT_RESET}\n"

# Форматирование только black
format:
	poetry run black $(SERVICE_DIR)/

# Запустить docker-compose с пересборкой и логами
start_docker:
	docker-compose down && docker-compose up --build -d && docker-compose logs -f

# Остановить docker-compose
stop_docker:
	docker-compose down

# Запуск приложения через poetry
start:
	poetry run python -m $(SERVICE_DIR)
