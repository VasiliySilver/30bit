"""
Pydantic схемы для User
"""
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, ConfigDict


class UserBase(BaseModel):
    """
    Базовая схема пользователя
    
    Attributes:
        email: Email пользователя
        display_name: Отображаемое имя
    """
    email: EmailStr = Field(..., description="Email пользователя")
    display_name: str = Field(..., min_length=1, max_length=255, description="Отображаемое имя")


class UserCreate(UserBase):
    """
    Схема для создания пользователя
    """
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "user@example.com",
                "display_name": "John Doe"
            }
        }
    )


class UserUpdate(BaseModel):
    """
    Схема для обновления пользователя
    
    Attributes:
        display_name: Новое отображаемое имя (опционально)
    """
    display_name: str | None = Field(None, min_length=1, max_length=255, description="Отображаемое имя")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "display_name": "Jane Doe"
            }
        }
    )


class UserResponse(UserBase):
    """
    Схема ответа с данными пользователя
    
    Attributes:
        id: ID пользователя
        created_at: Дата создания
    """
    id: int = Field(..., description="ID пользователя")
    created_at: datetime = Field(..., description="Дата создания")
    
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "email": "user@example.com",
                "display_name": "John Doe",
                "created_at": "2025-12-11T12:00:00"
            }
        }
    )