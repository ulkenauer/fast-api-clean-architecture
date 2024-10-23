# Выносится в отдельный модуль, подключается как зависимость
class DomainException(Exception):
    """
    Params:
        message* (string): Сообщение, которое можно отобразить пользователю
        code (string): Строковый код ошибки для отладки
    """

    def __init__(self, message: str, code: str) -> None:
        super().__init__()
        self.message = message
        self.code = code

    def __str__(self) -> str:
        return self.message


class ClientException(DomainException):
    pass


class AuthenticationException(DomainException):
    pass


class AuthorizationException(DomainException):
    pass


class ValidationException(DomainException):
    pass


class GatewayUnavailableException(DomainException):
    pass


class TimeoutException(DomainException):
    pass


class ObjectNotFoundException(DomainException):
    pass


class ConflictException(DomainException):
    pass
