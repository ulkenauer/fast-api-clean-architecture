import logging

from pythonjsonlogger.jsonlogger import JsonFormatter

from src.settings import DEBUG, STAGE

def setup_json_logging() -> logging.Logger:
    common_handler = logging.StreamHandler()

    if STAGE == "LOCAL":
        format_ = "%(levelname)s:%(name)s:%(asctime)s:%(message)s"
        datefmt = "%H:%M:%S"
        basic_formatter = logging.Formatter(format_, datefmt=datefmt)
        common_handler.setFormatter(basic_formatter)
    else:
        format_ = "%(timestamp)s %(level)s %(name)s %(message)s %(filename)s %(funcName)s %(lineno)s"
        json_formatter = JsonFormatter(format_, timestamp=True)
        common_handler.setFormatter(json_formatter)

    lib_logger = logging.getLogger("src")
    lib_logger.setLevel(logging.DEBUG if DEBUG else logging.INFO)
    lib_logger.addHandler(common_handler)
    lib_logger.propagate = False

    uvicorn_log = logging.getLogger("uvicorn")
    uvicorn_log.handlers = [common_handler]

    # set explicitly because the propagation is turned off
    uvicorn_access_log = logging.getLogger("uvicorn.access")
    uvicorn_access_log.handlers = [common_handler]

    # sentry_logger = logging.getLogger("sentry_sdk.errors")
    # sentry_logger.handlers = [common_handler]

    # set explicitly to avoid unparsable logs from the libraries
    # that call the basicConfig for themselves on initialization
    # logging.basicConfig(handlers=[common_handler], force=True)
    # might cause duplication of logs,
    # which may be avoided by turning off the propagation on child root package logger

    return lib_logger


lib_logger = setup_json_logging()
