"""
Общие Pydantic схемы
"""
from typing import Generic, TypeVar, List
from pydantic import BaseModel, Field

# Generic тип для данных в пагинированном ответе
T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    """
    Схема пагинированного ответа
    
    Attributes:
        items: Список элементов
        total: Общее количество элементов
        skip: Количество пропущенных элементов
        limit: Максимальное количество элементов на странице
    """
    items: List[T]
    total: int = Field(..., description="Общее количество элементов")
    skip: int = Field(..., ge=0, description="Количество пропущенных элементов")
    limit: int = Field(..., ge=1, description="Максимальное количество элементов")
    
    class Config:
        json_schema_extra = {
            "example": {
                "items": [],
                "total": 0,
                "skip": 0,
                "limit": 20
            }
        }


class ErrorResponse(BaseModel):
    """
    Схема ответа с ошибкой
    
    Attributes:
        error: Тип ошибки
        message: Сообщение об ошибке
        details: Дополнительные детали (опционально)
    """
    error: str = Field(..., description="Тип ошибки")
    message: str = Field(..., description="Сообщение об ошибке")
    details: dict | None = Field(None, description="Дополнительные детали")
    
    class Config:
        json_schema_extra = {
            "example": {
                "error": "ValidationError",
                "message": "Неверные данные",
                "details": {"field": "email", "issue": "Invalid format"}
            }
        }


class MessageResponse(BaseModel):
    """
    Схема простого ответа с сообщением
    
    Attributes:
        message: Сообщение
    """
    message: str = Field(..., description="Сообщение")
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "Операция выполнена успешно"
            }
        }