# Определяется для каждого компонента

from src.exceptions.exceptions import (
    DomainException,
    ObjectNotFoundException,
    ConflictException,
    GatewayUnavailableException,
    ClientException,
    ValidationException,
    AuthenticationException,
    AuthorizationException,
    TimeoutException,
)


class PostNotFoundException(ObjectNotFoundException):
    def __init__(self, post_id: str) -> None:
        message = f"Пост с идентификатором \"{post_id}\" не найден"
        code = "POST_NOT_FOUND"
        super().__init__(message=message, code=code)
