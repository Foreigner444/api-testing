from functools import lru_cache

from httpx import Client
from pydantic import BaseModel, ConfigDict, EmailStr

from clients.auth_client.authentication_client import get_authentication_client
from clients.auth_client.authentication_schema import LoginRequestSchema
from config import settings
from clients.event_hooks import curl_event_hook, log_request_event_hook, log_response_event_hook


class AuthenticationUserSchema(BaseModel):
    email: EmailStr
    password: str

    model_config = ConfigDict(frozen=True)


@lru_cache(maxsize=None)
def get_private_http_client(user: AuthenticationUserSchema) -> Client:
    auth_client = get_authentication_client()

    login_request = LoginRequestSchema(email=user.email, password=user.password)
    login_response = auth_client.login(request=login_request)

    return Client(
        base_url=settings.http_client.client_url,
        timeout=settings.http_client.timeout,
        headers={"Authorization": f"Bearer {login_response.token.access_token}"},
        event_hooks={
            "request": [curl_event_hook, log_request_event_hook],
            "response": [log_response_event_hook]
        }
    )

