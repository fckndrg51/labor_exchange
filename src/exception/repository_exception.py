class RepositoryException(Exception):
    """Базовое исключение для всех ошибок в репозитории."""
    pass


class NotFoundError(RepositoryException):
    """Вызывается, когда объект не найден в базе."""
    def __init__(self, entity_name: str, entity_id: int | None = None):
        message = f"{entity_name} не найден"
        if entity_id is not None:
            message += f" (id={entity_id})"
        super().__init__(message)