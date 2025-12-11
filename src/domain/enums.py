"""
Доменные перечисления для Reading List API
"""

from enum import Enum


class ItemKind(str, Enum):
    """Тип материала"""

    BOOK = "book"
    ARTICLE = "article"


class ItemStatus(str, Enum):
    """Статус прочтения материала"""

    PLANNED = "planned"
    READING = "reading"
    DONE = "done"


class Priority(str, Enum):
    """Приоритет материала"""

    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"


class SortOrder(str, Enum):
    """Порядок сортировки"""

    ASC = "asc"
    DESC = "desc"


class SortField(str, Enum):
    """Поля для сортировки"""

    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"
    PRIORITY = "priority"
