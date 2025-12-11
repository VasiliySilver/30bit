"""
Pydantic схемы для Tag
"""

from pydantic import BaseModel, ConfigDict, Field, field_validator


class TagBase(BaseModel):
    """
    Базовая схема тега

    Attributes:
        name: Название тега
    """

    name: str = Field(..., min_length=1, max_length=50, description="Название тега")

    @field_validator("name")
    @classmethod
    def normalize_name(cls, v: str) -> str:
        """Нормализовать название тега (убрать пробелы, привести к нижнему регистру)"""
        return v.strip().lower()


class TagCreate(TagBase):
    """
    Схема для создания тега
    """

    model_config = ConfigDict(json_schema_extra={"example": {"name": "python"}})


class TagResponse(TagBase):
    """
    Схема ответа с данными тега

    Attributes:
        id: ID тега
        user_id: ID пользователя-владельца
    """

    id: int = Field(..., description="ID тега")
    user_id: int = Field(..., description="ID пользователя-владельца")

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={"example": {"id": 1, "user_id": 1, "name": "python"}},
    )
