"""
API роутеры
"""

from src.api.routers.items import router as items_router
from src.api.routers.tags import router as tags_router

__all__ = ["items_router", "tags_router"]
