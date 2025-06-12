import sys
from pathlib import Path

import pytest


def main():
    """Запуск тестов."""
    # Добавляем корневую директорию проекта в PYTHONPATH
    project_root = Path(__file__).parent
    sys.path.insert(0, str(project_root))
    
    # Запускаем тесты
    pytest.main(["-v", "--cov=src", "--cov-report=term-missing"])


if __name__ == "__main__":
    main() 