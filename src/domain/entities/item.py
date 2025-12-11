"""
Доменная сущность Item
"""

from datetime import datetime, UTC
from dataclasses import dataclass
from typing import Optional

from src.domain.enums import ItemKind, ItemStatus, Priority


@dataclass
class Item:
    """
    Сущность материала (книга/статья)

    Attributes:
        id: Уникальный идентификатор
        user_id: ID пользователя-владельца
        title: Название материала
        kind: Тип материала (book|article)
        status: Статус прочтения (planned|reading|done)
        priority: Приоритет (low|normal|high)
        notes: Заметки (текст)
        created_at: Дата создания
        updated_at: Дата обновления
    """

    id: Optional[int]
    user_id: int
    title: str
    kind: ItemKind
    status: ItemStatus
    priority: Priority
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime

    def __post_init__(self):
        """Валидация после инициализации"""
        if not self.title or len(self.title.strip()) == 0:
            raise ValueError("Title не может быть пустым")

        if self.user_id <= 0:
            raise ValueError("User ID должен быть положительным числом")


        if self.updated_at < self.created_at:
            raise ValueError("Дата обновления не может быть раньше даты создания")

    def update(
        self,
        title: Optional[str] = None,
        kind: Optional[ItemKind] = None,
        status: Optional[ItemStatus] = None,
        priority: Optional[Priority] = None,
        notes: Optional[str] = None,
    ) -> None:
        """Обновление полей материала"""
        if title is not None:
            if not title or len(title.strip()) == 0:
                raise ValueError("Title не может быть пустым")
            self.title = title

        if kind is not None:
            self.kind = kind

        if status is not None:
            self.status = status

        if priority is not None:
            self.priority = priority

        if notes is not None:
            self.notes = notes

        self.updated_at = datetime.now(UTC)
