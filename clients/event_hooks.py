import allure
from tools.logger import get_logger
from httpx import Request, Response
from tools.http.curl import make_curl_from_request


logger = get_logger("HTTP_LOGGER")


def curl_event_hook(request: Request):
    curl_command = make_curl_from_request(request)

    allure.attach(curl_command, "cURL command", allure.attachment_type.TEXT)


def log_request_event_hook(request: Request):
    logger.info(
        f"Request: {request.method} {request.url}",
        extra={
            "type": "request",
            "method": request.method,
            "url": str(request.url),
            "headers": dict(request.headers),
        },
    )


def log_response_event_hook(response: Response):
    response.read()
    request = response.request
    logger.info(
        f"Response: {response.status_code} {response.reason_phrase} {request.method} from {request.url}",
        extra={
            "type": "response",
            "status_code": response.status_code,
            "url": str(request.url),
            "method": request.method,
            "headers": dict(response.headers),
            "elapsed_ms": response.elapsed.total_seconds() * 1000,
        },
    )