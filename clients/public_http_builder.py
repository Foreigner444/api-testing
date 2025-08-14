from httpx import Client
from config import settings
from clients.event_hooks import curl_event_hook, log_request_event_hook, log_response_event_hook


def get_public_client() -> Client:
    return Client(
        base_url=settings.http_client.client_url,
        timeout=settings.http_client.timeout,
        event_hooks={
            "request": [curl_event_hook, log_request_event_hook],
            "response": [log_response_event_hook]
        }
    )
