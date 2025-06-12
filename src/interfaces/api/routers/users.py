from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from tgbot_template.src.application.use_cases.user_management import UserManagementUseCase
from tgbot_template.src.domain.entities.user import User
from ..dependencies import get_user_management
from ..schemas import UserCreate, UserResponse, UserUpdate

router = APIRouter()


@router.get("/", response_model=List[UserResponse])
async def list_users(
    user_management: UserManagementUseCase = Depends(get_user_management),
) -> List[User]:
    """Получить список всех пользователей."""
    return await user_management.list_all()


@router.get("/active", response_model=List[UserResponse])
async def list_active_users(
    user_management: UserManagementUseCase = Depends(get_user_management),
) -> List[User]:
    """Получить список активных пользователей."""
    return await user_management.list_active()


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    user_management: UserManagementUseCase = Depends(get_user_management),
) -> User:
    """Получить пользователя по ID."""
    user = await user_management.get_user(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found",
        )
    return user


@router.get("/telegram/{telegram_id}", response_model=UserResponse)
async def get_user_by_telegram_id(
    telegram_id: int,
    user_management: UserManagementUseCase = Depends(get_user_management),
) -> User:
    """Получить пользователя по Telegram ID."""
    user = await user_management.get_user_by_telegram_id(telegram_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with telegram_id {telegram_id} not found",
        )
    return user


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    user_management: UserManagementUseCase = Depends(get_user_management),
) -> User:
    """Создать нового пользователя."""
    return await user_management.create_user(
        telegram_id=user_data.telegram_id,
        username=user_data.username,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
    )


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    user_management: UserManagementUseCase = Depends(get_user_management),
) -> User:
    """Обновить существующего пользователя."""
    user = await user_management.get_user(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found",
        )

    # Обновляем только переданные поля
    update_data = user_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)

    return await user_management.update_user(user)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    user_management: UserManagementUseCase = Depends(get_user_management),
) -> None:
    """Удалить пользователя."""
    user = await user_management.get_user(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found",
        )
    await user_management.delete_user(user_id) 