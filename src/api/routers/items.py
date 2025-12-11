"""
API роутер для работы с материалами
"""

from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status

from src.api.dependencies import get_current_user_id, get_item_service
from src.application.schemas.common import ErrorResponse, MessageResponse
from src.application.schemas.item import ItemCreate, ItemResponse, ItemUpdate
from src.application.services.item_service import ItemService
from src.domain.enums import ItemKind, ItemStatus, Priority
from src.domain.exceptions import EntityNotFoundError, PermissionDeniedError

router = APIRouter(prefix="/items", tags=["items"])


@router.post(
    "",
    response_model=ItemResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Создать новый материал",
    responses={
        201: {"description": "Материал успешно создан"},
        403: {"model": ErrorResponse, "description": "Доступ к тегам запрещен"},
    },
)
async def create_item(
    data: ItemCreate,
    user_id: int = Depends(get_current_user_id),
    item_service: ItemService = Depends(get_item_service),
) -> ItemResponse:
    """
    Создать новый материал для текущего пользователя
    """
    try:
        return await item_service.create_item(user_id, data)
    except PermissionDeniedError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"error": "PermissionDeniedError", "message": e.message},
        )


@router.get(
    "",
    response_model=List[ItemResponse],
    summary="Получить список материалов пользователя",
    responses={200: {"description": "Список материалов"}},
)
async def get_items(
    skip: int = Query(0, ge=0, description="Количество пропускаемых записей"),
    limit: int = Query(20, ge=1, le=100, description="Максимальное количество записей"),
    kind: Optional[ItemKind] = Query(None, description="Фильтр по типу материала"),
    status: Optional[ItemStatus] = Query(None, description="Фильтр по статусу"),
    priority: Optional[Priority] = Query(None, description="Фильтр по приоритету"),
    tag_ids: Optional[List[int]] = Query(
        None, description="Фильтр по тегам (любая из указанных)"
    ),
    title_contains: Optional[str] = Query(None, description="Подстрока в названии"),
    created_from: Optional[datetime] = Query(None, description="Дата создания от"),
    created_to: Optional[datetime] = Query(None, description="Дата создания до"),
    sort_by: str = Query(
        "created_at", description="Поле сортировки (created_at|updated_at|priority)"
    ),
    sort_order: str = Query("desc", description="Порядок сортировки (asc|desc)"),
    user_id: int = Depends(get_current_user_id),
    item_service: ItemService = Depends(get_item_service),
) -> List[ItemResponse]:
    """
    Получить все материалы текущего пользователя с возможностью фильтрации
    """
    return await item_service.get_user_items(
        user_id=user_id,
        skip=skip,
        limit=limit,
        kind=kind,
        status=status,
        priority=priority,
        tag_ids=tag_ids,
        title_contains=title_contains,
        created_from=created_from,
        created_to=created_to,
        sort_by=sort_by,
        sort_order=sort_order,
    )


@router.get(
    "/{item_id}",
    response_model=ItemResponse,
    summary="Получить материал по ID",
    responses={
        200: {"description": "Данные материала"},
        403: {"model": ErrorResponse, "description": "Доступ запрещен"},
        404: {"model": ErrorResponse, "description": "Материал не найден"},
    },
)
async def get_item(
    item_id: int,
    user_id: int = Depends(get_current_user_id),
    item_service: ItemService = Depends(get_item_service),
) -> ItemResponse:
    """
    Получить материал по ID
    """
    try:
        return await item_service.get_item(item_id, user_id)
    except EntityNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "EntityNotFoundError", "message": e.message},
        )
    except PermissionDeniedError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"error": "PermissionDeniedError", "message": e.message},
        )


@router.put(
    "/{item_id}",
    response_model=ItemResponse,
    summary="Обновить материал",
    responses={
        200: {"description": "Материал успешно обновлен"},
        403: {"model": ErrorResponse, "description": "Доступ запрещен"},
        404: {"model": ErrorResponse, "description": "Материал не найден"},
    },
)
async def update_item(
    item_id: int,
    data: ItemUpdate,
    user_id: int = Depends(get_current_user_id),
    item_service: ItemService = Depends(get_item_service),
) -> ItemResponse:
    """
    Обновить материал
    """
    try:
        return await item_service.update_item(item_id, user_id, data)
    except EntityNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "EntityNotFoundError", "message": e.message},
        )
    except PermissionDeniedError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"error": "PermissionDeniedError", "message": e.message},
        )


@router.post(
    "/{item_id}/tags",
    response_model=MessageResponse,
    summary="Добавить теги к материалу",
    responses={
        200: {"description": "Теги успешно добавлены"},
        403: {"model": ErrorResponse, "description": "Доступ запрещен"},
        404: {"model": ErrorResponse, "description": "Материал не найден"},
    },
)
async def add_tags_to_item(
    item_id: int,
    tag_ids: List[int],
    user_id: int = Depends(get_current_user_id),
    item_service: ItemService = Depends(get_item_service),
) -> MessageResponse:
    """
    Добавить теги к материалу
    """
    try:
        # Добавляем теги
        await item_service.add_tags_to_item(item_id, tag_ids, user_id)

        return MessageResponse(message="Теги успешно добавлены к материалу")
    except EntityNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "EntityNotFoundError", "message": e.message},
        )
    except PermissionDeniedError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"error": "PermissionDeniedError", "message": e.message},
        )


@router.delete(
    "/{item_id}/tags",
    response_model=MessageResponse,
    summary="Удалить теги у материала",
    responses={
        200: {"description": "Теги успешно удалены"},
        403: {"model": ErrorResponse, "description": "Доступ запрещен"},
        404: {"model": ErrorResponse, "description": "Материал не найден"},
    },
)
async def remove_tags_from_item(
    item_id: int,
    tag_ids: List[int],
    user_id: int = Depends(get_current_user_id),
    item_service: ItemService = Depends(get_item_service),
) -> MessageResponse:
    """
    Удалить теги у материала
    """
    try:
        # Удаляем теги
        await item_service.remove_tags_from_item(item_id, tag_ids, user_id)

        return MessageResponse(message="Теги успешно удалены у материала")
    except EntityNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "EntityNotFoundError", "message": e.message},
        )
    except PermissionDeniedError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"error": "PermissionDeniedError", "message": e.message},
        )


@router.delete(
    "/{item_id}",
    response_model=MessageResponse,
    summary="Удалить материал",
    responses={
        200: {"description": "Материал успешно удален"},
        403: {"model": ErrorResponse, "description": "Доступ запрещен"},
        404: {"model": ErrorResponse, "description": "Материал не найден"},
    },
)
async def delete_item(
    item_id: int,
    user_id: int = Depends(get_current_user_id),
    item_service: ItemService = Depends(get_item_service),
) -> MessageResponse:
    """
    Удалить материал
    """
    try:
        await item_service.delete_item(item_id, user_id)
        return MessageResponse(message="Материал успешно удален")
    except EntityNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "EntityNotFoundError", "message": e.message},
        )
    except PermissionDeniedError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"error": "PermissionDeniedError", "message": e.message},
        )
