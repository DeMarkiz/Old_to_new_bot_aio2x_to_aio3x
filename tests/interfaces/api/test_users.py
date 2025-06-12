import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

from src.interfaces.api.main import create_app
from tests.conftest import TEST_USER


@pytest.fixture
def client():
    """Создание тестового клиента."""
    app = create_app()
    return TestClient(app)


@pytest.fixture
async def async_client():
    """Создание асинхронного тестового клиента."""
    app = create_app()
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.mark.asyncio
async def test_list_users(async_client, test_user):
    """Тест получения списка пользователей."""
    response = await async_client.get("/api/v1/users/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert any(user["id"] == test_user.id for user in data)


@pytest.mark.asyncio
async def test_list_active_users(async_client, test_user):
    """Тест получения списка активных пользователей."""
    response = await async_client.get("/api/v1/users/active")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert any(user["id"] == test_user.id for user in data)
    assert all(user["is_active"] for user in data)


@pytest.mark.asyncio
async def test_get_user(async_client, test_user):
    """Тест получения пользователя по ID."""
    response = await async_client.get(f"/api/v1/users/{test_user.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_user.id
    assert data["telegram_id"] == test_user.telegram_id
    assert data["username"] == test_user.username


@pytest.mark.asyncio
async def test_get_user_by_telegram_id(async_client, test_user):
    """Тест получения пользователя по Telegram ID."""
    response = await async_client.get(f"/api/v1/users/telegram/{test_user.telegram_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_user.id
    assert data["telegram_id"] == test_user.telegram_id
    assert data["username"] == test_user.username


@pytest.mark.asyncio
async def test_create_user(async_client):
    """Тест создания пользователя."""
    user_data = {
        "telegram_id": 987654321,
        "username": "new_user",
        "first_name": "New",
        "last_name": "User",
    }
    response = await async_client.post("/api/v1/users/", json=user_data)
    assert response.status_code == 201
    data = response.json()
    assert data["telegram_id"] == user_data["telegram_id"]
    assert data["username"] == user_data["username"]
    assert data["first_name"] == user_data["first_name"]
    assert data["last_name"] == user_data["last_name"]
    assert data["is_active"] is True
    assert data["is_admin"] is False


@pytest.mark.asyncio
async def test_update_user(async_client, test_user):
    """Тест обновления пользователя."""
    update_data = {
        "username": "updated_username",
        "first_name": "Updated",
        "last_name": "User",
        "is_active": False,
        "is_admin": True,
    }
    response = await async_client.put(f"/api/v1/users/{test_user.id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_user.id
    assert data["username"] == update_data["username"]
    assert data["first_name"] == update_data["first_name"]
    assert data["last_name"] == update_data["last_name"]
    assert data["is_active"] == update_data["is_active"]
    assert data["is_admin"] == update_data["is_admin"]


@pytest.mark.asyncio
async def test_delete_user(async_client, test_user):
    """Тест удаления пользователя."""
    response = await async_client.delete(f"/api/v1/users/{test_user.id}")
    assert response.status_code == 204
    
    # Проверяем, что пользователь удален
    response = await async_client.get(f"/api/v1/users/{test_user.id}")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_user_not_found(async_client):
    """Тест получения несуществующего пользователя."""
    response = await async_client.get("/api/v1/users/999")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_user_by_telegram_id_not_found(async_client):
    """Тест получения несуществующего пользователя по Telegram ID."""
    response = await async_client.get("/api/v1/users/telegram/999")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_create_user_validation(async_client):
    """Тест валидации при создании пользователя."""
    # Отправляем неполные данные
    user_data = {
        "username": "new_user",
        "first_name": "New",
    }
    response = await async_client.post("/api/v1/users/", json=user_data)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_update_user_validation(async_client, test_user):
    """Тест валидации при обновлении пользователя."""
    # Отправляем неверные данные
    update_data = {
        "telegram_id": "invalid",  # Должно быть числом
        "is_active": "invalid",    # Должно быть булевым значением
    }
    response = await async_client.put(f"/api/v1/users/{test_user.id}", json=update_data)
    assert response.status_code == 422 