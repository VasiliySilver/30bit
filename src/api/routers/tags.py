"""
API роутер для работы с тегами
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query

from src.application.services.tag_service import TagService
from src.application.schemas.tag import TagCreate, TagResponse
from src.application.schemas.common import MessageResponse, ErrorResponse
from src.domain.exceptions import EntityNotFoundError, DuplicateEntityError, PermissionDeniedError
from src.api.dependencies import get_tag_service, get_current_user_id

router = APIRouter(prefix="/tags", tags=["tags"])


@router.post(
    "",
    response_model=TagResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Создать новый тег",
    responses={
        201: {"description": "Тег успешно создан"},
        409: {"model": ErrorResponse, "description": "Тег с таким именем уже существует"}
    }
)
async def create_tag(
    data: TagCreate,
    user_id: int = Depends(get_current_user_id),
    tag_service: TagService = Depends(get_tag_service)
) -> TagResponse:
    """
    Создать новый тег для текущего пользователя
    """
    try:
        return await tag_service.create_tag(user_id, data)
    except DuplicateEntityError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"error": "DuplicateEntityError", "message": e.message}
        )


@router.get(
    "",
    response_model=List[TagResponse],
    summary="Получить список тегов пользователя",
    responses={
        200: {"description": "Список тегов"}
    }
)
async def get_tags(
    skip: int = Query(0, ge=0, description="Количество пропускаемых записей"),
    limit: int = Query(20, ge=1, le=100, description="Максимальное количество записей"),
    user_id: int = Depends(get_current_user_id),
    tag_service: TagService = Depends(get_tag_service)
) -> List[TagResponse]:
    """
    Получить все теги текущего пользователя
    """
    return await tag_service.get_user_tags(user_id, skip, limit)


@router.get(
    "/{tag_id}",
    response_model=TagResponse,
    summary="Получить тег по ID",
    responses={
        200: {"description": "Данные тега"},
        403: {"model": ErrorResponse, "description": "Доступ запрещен"},
        404: {"model": ErrorResponse, "description": "Тег не найден"}
    }
)
async def get_tag(
    tag_id: int,
    user_id: int = Depends(get_current_user_id),
    tag_service: TagService = Depends(get_tag_service)
) -> TagResponse:
    """
    Получить тег по ID
    """
    try:
        return await tag_service.get_tag(tag_id, user_id)
    except EntityNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "EntityNotFoundError", "message": e.message}
        )
    except PermissionDeniedError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"error": "PermissionDeniedError", "message": e.message}
        )


@router.delete(
    "/{tag_id}",
    response_model=MessageResponse,
    summary="Удалить тег",
    responses={
        200: {"description": "Тег успешно удален"},
        403: {"model": ErrorResponse, "description": "Доступ запрещен"},
        404: {"model": ErrorResponse, "description": "Тег не найден"}
    }
)
async def delete_tag(
    tag_id: int,
    user_id: int = Depends(get_current_user_id),
    tag_service: TagService = Depends(get_tag_service)
) -> MessageResponse:
    """
    Удалить тег
    """
    try:
        await tag_service.delete_tag(tag_id, user_id)
        return MessageResponse(message="Тег успешно удален")
    except EntityNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "EntityNotFoundError", "message": e.message}
        )
    except PermissionDeniedError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"error": "PermissionDeniedError", "message": e.message}
        )