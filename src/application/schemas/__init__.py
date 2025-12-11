"""
Pydantic схемы для API
"""

from src.application.schemas.common import (
    ErrorResponse,
    MessageResponse,
    PaginatedResponse,
)
from src.application.schemas.item import (
    ItemCreate,
    ItemFilterParams,
    ItemResponse,
    ItemUpdate,
)
from src.application.schemas.tag import TagCreate, TagResponse
from src.application.schemas.user import UserCreate, UserResponse, UserUpdate

__all__ = [
    # Common
    "PaginatedResponse",
    "ErrorResponse",
    "MessageResponse",
    # User
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    # Tag
    "TagCreate",
    "TagResponse",
    # Item
    "ItemCreate",
    "ItemUpdate",
    "ItemResponse",
    "ItemFilterParams",
]
