# Выносится в отдельный модуль, подключается как зависимость

import logging
import traceback
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

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

logger = logging.getLogger(__name__)


class HTTPExceptionMapper:
    @staticmethod
    def _to_json(exception: DomainException) -> dict:
        return {
            "message": exception.message,
            "code": exception.code,
        }

    @staticmethod
    def _log_exception(exception: DomainException) -> None:
        # logger.error("".join(traceback.format_tb(exception.__traceback__)))
        # logger.error("".join(traceback.format_tb(exception.__cause__.__traceback__)))
        logger.error("".join(traceback.format_exception(exception, chain=True)))
        # traceback.format_exception()

    @staticmethod
    def map_object_not_found_exception(request: Request, exception: ObjectNotFoundException) -> JSONResponse:
        HTTPExceptionMapper._log_exception(exception)
        return JSONResponse(content=HTTPExceptionMapper._to_json(exception), status_code=404)

    @staticmethod
    def map_conflict_exception(request: Request, exception: ConflictException) -> JSONResponse:
        HTTPExceptionMapper._log_exception(exception)
        return JSONResponse(content=HTTPExceptionMapper._to_json(exception), status_code=409)

    @staticmethod
    def map_client_exception(request: Request, exception: ClientException) -> JSONResponse:
        HTTPExceptionMapper._log_exception(exception)
        return JSONResponse(content=HTTPExceptionMapper._to_json(exception), status_code=400)

    @staticmethod
    def map_authentication_exception(request: Request, exception: AuthenticationException) -> JSONResponse:
        HTTPExceptionMapper._log_exception(exception)
        return JSONResponse(content=HTTPExceptionMapper._to_json(exception), status_code=401)

    @staticmethod
    def map_authorization_exception(request: Request, exception: AuthorizationException) -> JSONResponse:
        HTTPExceptionMapper._log_exception(exception)
        return JSONResponse(content=HTTPExceptionMapper._to_json(exception), status_code=403)

    @staticmethod
    def map_validation_exception(request: Request, exception: ValidationException) -> JSONResponse:
        HTTPExceptionMapper._log_exception(exception)
        return JSONResponse(content=HTTPExceptionMapper._to_json(exception), status_code=422)

    @staticmethod
    def map_gateway_unavailable_exception(request: Request, exception: GatewayUnavailableException) -> JSONResponse:
        HTTPExceptionMapper._log_exception(exception)
        return JSONResponse(content=HTTPExceptionMapper._to_json(exception), status_code=502)

    @staticmethod
    def map_timeout_exception(request: Request, exception: TimeoutException) -> JSONResponse:
        HTTPExceptionMapper._log_exception(exception)
        return JSONResponse(content=HTTPExceptionMapper._to_json(exception), status_code=504)


def add_domain_exceptions_handlers(app: FastAPI) -> None:
    app.add_exception_handler(ObjectNotFoundException, HTTPExceptionMapper.map_object_not_found_exception)
    app.add_exception_handler(ConflictException, HTTPExceptionMapper.map_conflict_exception)
    app.add_exception_handler(GatewayUnavailableException, HTTPExceptionMapper.map_gateway_unavailable_exception)
    app.add_exception_handler(ClientException, HTTPExceptionMapper.map_client_exception)
    app.add_exception_handler(ValidationException, HTTPExceptionMapper.map_validation_exception)
    app.add_exception_handler(AuthenticationException, HTTPExceptionMapper.map_authentication_exception)
    app.add_exception_handler(AuthorizationException, HTTPExceptionMapper.map_authorization_exception)
    app.add_exception_handler(TimeoutException, HTTPExceptionMapper.map_timeout_exception)
