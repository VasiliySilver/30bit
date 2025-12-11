"""
Доменные исключения для Reading List API
"""


class DomainException(Exception):
    """Базовое доменное исключение"""

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class EntityNotFoundError(DomainException):
    """Исключение: сущность не найдена"""

    def __init__(self, entity_name: str, entity_id: int):
        super().__init__(f"{entity_name} с id={entity_id} не найден")
        self.entity_name = entity_name
        self.entity_id = entity_id


class DuplicateEntityError(DomainException):
    """Исключение: дубликат сущности"""

    def __init__(self, entity_name: str, field: str, value: str):
        super().__init__(f"{entity_name} с {field}='{value}' уже существует")
        self.entity_name = entity_name
        self.field = field
        self.value = value


class ValidationError(DomainException):
    """Исключение: ошибка валидации"""

    def __init__(self, message: str):
        super().__init__(message)


class PermissionDeniedError(DomainException):
    """Исключение: доступ запрещен"""

    def __init__(self, message: str = "Доступ запрещен"):
        super().__init__(message)
