"""
API роутер для работы с пользователями
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query

from src.infrastructure.repositories.user_repository import UserRepository
from src.application.schemas.user import UserCreate, UserUpdate, UserResponse
from src.application.schemas.common import MessageResponse, ErrorResponse
from src.api.dependencies import get_user_repository

router = APIRouter(prefix="/users", tags=["users"])


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Создать нового пользователя",
    responses={
        201: {"description": "Пользователь успешно создан"},
        409: {
            "model": ErrorResponse,
            "description": "Пользователь с таким email уже существует",
        },
    },
)
async def create_user(
    data: UserCreate, user_repo: UserRepository = Depends(get_user_repository)
) -> UserResponse:
    """
    Создать нового пользователя
    """
    if await user_repo.exists_by_email(data.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "error": "DuplicateEntityError",
                "message": "Пользователь с таким email уже существует",
            },
        )
    user = await user_repo.create(data)
    return await user_repo.to_entity(user)


@router.get(
    "",
    response_model=List[UserResponse],
    summary="Получить список пользователей",
    responses={200: {"description": "Список пользователей"}},
)
async def get_users(
    skip: int = Query(0, ge=0, description="Количество пропускаемых записей"),
    limit: int = Query(20, ge=1, le=100, description="Максимальное количество записей"),
    user_repo: UserRepository = Depends(get_user_repository),
) -> List[UserResponse]:
    """
    Получить всех пользователей
    """
    users = await user_repo.get_all(skip=skip, limit=limit)
    return users


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Получить пользователя по ID",
    responses={
        200: {"description": "Данные пользователя"},
        404: {"model": ErrorResponse, "description": "Пользователь не найден"},
    },
)
async def get_user(
    user_id: int, user_repo: UserRepository = Depends(get_user_repository)
) -> UserResponse:
    """
    Получить пользователя по ID
    """
    user = await user_repo.get_by_id(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": "EntityNotFoundError",
                "message": "Пользователь не найден",
            },
        )
    return user


@router.put(
    "/{user_id}",
    response_model=UserResponse,
    summary="Обновить пользователя",
    responses={
        200: {"description": "Пользователь успешно обновлен"},
        404: {"model": ErrorResponse, "description": "Пользователь не найден"},
    },
)
async def update_user(
    user_id: int,
    data: UserUpdate,
    user_repo: UserRepository = Depends(get_user_repository),
) -> UserResponse:
    """
    Обновить пользователя
    """
    user = await user_repo.get_by_id(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": "EntityNotFoundError",
                "message": "Пользователь не найден",
            },
        )
    # Обновляем поля
    if data.display_name:
        user.display_name = data.display_name
    updated_user = await user_repo.update(user)
    return updated_user


@router.delete(
    "/{user_id}",
    response_model=MessageResponse,
    summary="Удалить пользователя",
    responses={
        200: {"description": "Пользователь успешно удален"},
        404: {"model": ErrorResponse, "description": "Пользователь не найден"},
    },
)
async def delete_user(
    user_id: int, user_repo: UserRepository = Depends(get_user_repository)
) -> MessageResponse:
    """
    Удалить пользователя
    """
    deleted = await user_repo.delete(user_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": "EntityNotFoundError",
                "message": "Пользователь не найден",
            },
        )
    return MessageResponse(message="Пользователь успешно удален")
