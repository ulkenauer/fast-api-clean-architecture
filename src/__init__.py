import fastapi
import sentry_sdk

from src.exceptions.fast_api_exception_mapper import add_domain_exceptions_handlers
from src.logging import lib_logger
from src.settings import DEBUG
from src.posts.presentation.http.views import posts_router


async def on_app_startup() -> None:
    sentry_sdk.init(
        debug=DEBUG,
        release="0.0.0",
        traces_sample_rate=1.0,
    )


def assemble_app() -> fastapi.FastAPI:
    application = fastapi.FastAPI(
        version="0.0.0",
    )

    application.include_router(posts_router)

    application.add_event_handler("startup", on_app_startup)

    add_domain_exceptions_handlers(application)

    application.logger = lib_logger

    return application


app = assemble_app()
