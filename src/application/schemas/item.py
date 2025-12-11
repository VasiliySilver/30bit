"""
Pydantic схемы для Item
"""

from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional

from src.domain.enums import ItemKind, ItemStatus, Priority


class ItemBase(BaseModel):
    """
    Базовая схема материала

    Attributes:
        title: Название материала
        kind: Тип материала (book|article)
        status: Статус прочтения (planned|reading|done)
        priority: Приоритет (low|normal|high)
        notes: Заметки
    """

    title: str = Field(
        ..., min_length=1, max_length=500, description="Название материала"
    )
    kind: ItemKind = Field(..., description="Тип материала")
    status: ItemStatus = Field(
        default=ItemStatus.PLANNED, description="Статус прочтения"
    )
    priority: Priority = Field(default=Priority.NORMAL, description="Приоритет")
    notes: Optional[str] = Field(None, description="Заметки")


class ItemCreate(ItemBase):
    """
    Схема для создания материала

    Attributes:
        tag_ids: Список ID тегов для материала
    """

    tag_ids: List[int] = Field(default_factory=list, description="Список ID тегов")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Clean Code",
                "kind": "book",
                "status": "planned",
                "priority": "high",
                "notes": "Must read for software developers",
                "tag_ids": [1, 2],
            }
        }
    )


class ItemUpdate(BaseModel):
    """
    Схема для обновления материала

    Все поля опциональны
    """

    title: Optional[str] = Field(
        None, min_length=1, max_length=500, description="Название материала"
    )
    kind: Optional[ItemKind] = Field(None, description="Тип материала")
    status: Optional[ItemStatus] = Field(None, description="Статус прочтения")
    priority: Optional[Priority] = Field(None, description="Приоритет")
    notes: Optional[str] = Field(None, description="Заметки")
    tag_ids: Optional[List[int]] = Field(
        None, description="Список ID тегов (заменит существующие)"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "status": "reading",
                "notes": "Started reading chapter 1",
                "tag_ids": [1, 3],
            }
        }
    )


class ItemResponse(ItemBase):
    """
    Схема ответа с данными материала

    Attributes:
        id: ID материала
        user_id: ID пользователя-владельца
        created_at: Дата создания
        updated_at: Дата обновления
        tag_ids: Список ID тегов
    """

    id: int = Field(..., description="ID материала")
    user_id: int = Field(..., description="ID пользователя-владельца")
    created_at: datetime = Field(..., description="Дата создания")
    updated_at: datetime = Field(..., description="Дата обновления")
    tag_ids: List[int] = Field(default_factory=list, description="Список ID тегов")

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "user_id": 1,
                "title": "Clean Code",
                "kind": "book",
                "status": "reading",
                "priority": "high",
                "notes": "Started reading chapter 1",
                "created_at": "2025-12-11T12:00:00",
                "updated_at": "2025-12-11T14:30:00",
                "tag_ids": [1, 3],
            }
        },
    )


class ItemFilterParams(BaseModel):
    """
    Параметры фильтрации для списка материалов

    Attributes:
        kind: Фильтр по типу материала
        status: Фильтр по статусу
        priority: Фильтр по приоритету
        skip: Количество пропускаемых записей
        limit: Максимальное количество записей
    """

    kind: Optional[ItemKind] = Field(None, description="Фильтр по типу материала")
    status: Optional[ItemStatus] = Field(None, description="Фильтр по статусу")
    priority: Optional[Priority] = Field(None, description="Фильтр по приоритету")
    skip: int = Field(0, ge=0, description="Количество пропускаемых записей")
    limit: int = Field(20, ge=1, le=100, description="Максимальное количество записей")
