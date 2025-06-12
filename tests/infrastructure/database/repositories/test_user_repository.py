import pytest
from sqlalchemy import select

from src.domain.entities.user import User
from src.infrastructure.database.models import UserModel
from tests.conftest import TEST_USER


@pytest.mark.asyncio
async def test_create_user(user_repository, test_session):
    """Тест создания пользователя."""
    # Создаем пользователя
    user = await user_repository.create_user(
        telegram_id=TEST_USER.telegram_id,
        username=TEST_USER.username,
        first_name=TEST_USER.first_name,
        last_name=TEST_USER.last_name,
    )
    
    # Проверяем, что пользователь создан
    assert user.id is not None
    assert user.telegram_id == TEST_USER.telegram_id
    assert user.username == TEST_USER.username
    assert user.first_name == TEST_USER.first_name
    assert user.last_name == TEST_USER.last_name
    assert user.is_active is True
    assert user.is_admin is False
    assert user.created_at is not None
    assert user.updated_at is not None


@pytest.mark.asyncio
async def test_get_user_by_id(user_repository, test_user):
    """Тест получения пользователя по ID."""
    # Получаем пользователя
    user = await user_repository.get_user_by_id(test_user.id)
    
    # Проверяем, что пользователь найден
    assert user is not None
    assert user.id == test_user.id
    assert user.telegram_id == test_user.telegram_id
    assert user.username == test_user.username


@pytest.mark.asyncio
async def test_get_user_by_telegram_id(user_repository, test_user):
    """Тест получения пользователя по Telegram ID."""
    # Получаем пользователя
    user = await user_repository.get_user_by_telegram_id(test_user.telegram_id)
    
    # Проверяем, что пользователь найден
    assert user is not None
    assert user.id == test_user.id
    assert user.telegram_id == test_user.telegram_id
    assert user.username == test_user.username


@pytest.mark.asyncio
async def test_get_all_users(user_repository, test_user):
    """Тест получения всех пользователей."""
    # Получаем всех пользователей
    users = await user_repository.get_all_users()
    
    # Проверяем, что список не пустой и содержит тестового пользователя
    assert len(users) > 0
    assert any(user.id == test_user.id for user in users)


@pytest.mark.asyncio
async def test_get_active_users(user_repository, test_user):
    """Тест получения активных пользователей."""
    # Получаем активных пользователей
    users = await user_repository.get_active_users()
    
    # Проверяем, что список не пустой и содержит тестового пользователя
    assert len(users) > 0
    assert any(user.id == test_user.id for user in users)
    assert all(user.is_active for user in users)


@pytest.mark.asyncio
async def test_update_user(user_repository, test_user):
    """Тест обновления пользователя."""
    # Обновляем пользователя
    updated_user = await user_repository.update_user(
        test_user.id,
        username="updated_username",
        first_name="Updated",
        last_name="User",
        is_active=False,
        is_admin=True,
    )
    
    # Проверяем, что пользователь обновлен
    assert updated_user.id == test_user.id
    assert updated_user.username == "updated_username"
    assert updated_user.first_name == "Updated"
    assert updated_user.last_name == "User"
    assert updated_user.is_active is False
    assert updated_user.is_admin is True


@pytest.mark.asyncio
async def test_delete_user(user_repository, test_user):
    """Тест удаления пользователя."""
    # Удаляем пользователя
    await user_repository.delete_user(test_user.id)
    
    # Проверяем, что пользователь удален
    user = await user_repository.get_user_by_id(test_user.id)
    assert user is None


@pytest.mark.asyncio
async def test_get_user_by_id_not_found(user_repository):
    """Тест получения несуществующего пользователя по ID."""
    # Пытаемся получить несуществующего пользователя
    user = await user_repository.get_user_by_id(999)
    
    # Проверяем, что пользователь не найден
    assert user is None


@pytest.mark.asyncio
async def test_get_user_by_telegram_id_not_found(user_repository):
    """Тест получения несуществующего пользователя по Telegram ID."""
    # Пытаемся получить несуществующего пользователя
    user = await user_repository.get_user_by_telegram_id(999)
    
    # Проверяем, что пользователь не найден
    assert user is None 