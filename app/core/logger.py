import logging
import time
from typing import Callable

import graypy
from fastapi import Request, Response
from fastapi.routing import APIRoute

from app.core.config import settings


class TimedRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            before = time.time()
            j = None
            try:
                j = await request.json()
            except Exception:
                pass
            log.debug(f"REQUEST: {request.method}, {request.url.path}, body: {j}")
            response: Response = await original_route_handler(request)
            duration = time.time() - before
            response.headers["X-Response-Time"] = str(duration)
            try:
                j = response.body
            except Exception:
                j = None
            log.debug(f"RESPONSE: [{duration}] => {j}")
            return response

        return custom_route_handler


def create_logger():
    """
    Setup the logging environment
    """
    log = logging.getLogger(__name__)  # root logger
    log.setLevel(logging.DEBUG)
    format_str = "%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)s - %(funcName)s() ] - %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"

    formatter = logging.Formatter(format_str, date_format)

    if settings.CONFIG_TYPE == "prod":
        handler = graypy.GELFUDPHandler(
            settings.GRAYLOG_SERVER,
            settings.GRAYLOG_PORT,
            localname=settings.DEPLOYMENT,
        )
        handler.setFormatter(formatter)
        log.addHandler(handler)

    handler = logging.StreamHandler()

    handler.setFormatter(formatter)
    log.addHandler(handler)
    log.propagate = False

    my_adapter = logging.LoggerAdapter(log, {"tag": settings.APPLICATION_NAME})

    return my_adapter


log = create_logger()
