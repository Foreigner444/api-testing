import logging
import sys

from httpx import Request, Response
from pythonjsonlogger import json

logger = logging.getLogger()

logger.setLevel(logging.INFO)

logHandler = logging.StreamHandler(sys.stdout)

formatter = json.JsonFormatter("%(message)s")
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)


def log_request(request: Request):
    logger.info(
        f"Request: {request.method} {request.url}",
        extra={
            "type": "request",
            "method": request.method,
            "url": str(request.url),
            "headers": dict(request.headers),
        },
    )


def log_response(response: Response):
    response.read()
    request = response.request
    logger.info(
        f"Response: {response.status_code} {request.method} {request.url}",
        extra={
            "type": "response",
            "status_code": response.status_code,
            "url": str(request.url),
            "method": request.method,
            "headers": dict(response.headers),
            "elapsed_ms": response.elapsed.total_seconds() * 1000,
        },
    )
